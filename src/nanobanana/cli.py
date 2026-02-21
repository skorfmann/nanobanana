"""CLI entry point for nanobanana."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from nanobanana import __version__
from nanobanana.config import load_config, resolve_config
from nanobanana.mime import extension_from_mime
from nanobanana.slide_templates import SLIDE_TEMPLATES, format_slide_help, get_slide_template
from nanobanana.templates import (
    COMMANDS,
    format_command_help,
    format_help_overview,
    get_command,
)

# All known subcommand names plus pseudo-commands
_KNOWN_COMMANDS = frozenset(COMMANDS) | {"help", "version"}

# Flags that consume the next argument as their value
_VALUE_FLAGS = frozenset({"-i", "-o", "-aspect", "-size", "-model"})


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with single-dash long flags."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-i", action="append", default=[], dest="input_images",
                        help="Input image file (repeatable)")
    parser.add_argument("-o", default="", dest="output",
                        help="Output filename")
    parser.add_argument("-aspect", default="", dest="aspect",
                        help="Aspect ratio")
    parser.add_argument("-size", default="", dest="size",
                        help="Image size")
    parser.add_argument("-model", default="", dest="model",
                        help="OpenRouter model")
    parser.add_argument("-h", action="store_true", dest="show_help",
                        help="Show help")
    parser.add_argument("-version", action="store_true", dest="show_version",
                        help="Show version")
    parser.add_argument("prompt", nargs="*", help="Generation prompt")
    return parser


def _extract_subcommand(argv: list[str]) -> tuple[str, list[str]]:
    """Extract subcommand from argv if the first non-flag arg is a known command.

    Returns (command_name, remaining_argv). If no subcommand found,
    returns ("", original_argv).
    """
    # Find the first positional argument (not starting with -)
    skip_next = False
    for idx, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        if arg.startswith("-"):
            if arg in _VALUE_FLAGS:
                skip_next = True  # next arg is the flag's value, not a positional
            continue
        if arg in _KNOWN_COMMANDS:
            return arg, argv[:idx] + argv[idx + 1:]
        # First positional arg is not a command — treat as free prompt
        break
    return "", argv


def print_usage() -> None:
    """Print usage text to stderr."""
    sys.stderr.write(format_help_overview())


def run(argv: list[str] | None = None) -> None:
    """Main CLI logic. Raises RuntimeError on errors."""
    if argv is None:
        argv = sys.argv[1:]

    # Extract subcommand before argparse sees the args
    command_name, remaining_argv = _extract_subcommand(argv)

    parser = build_parser()
    args = parser.parse_args(remaining_argv)

    # Handle pseudo-commands
    if command_name == "version" or args.show_version:
        print(f"nanobanana {__version__}")
        return

    if command_name == "help" or args.show_help:
        # "nanobanana help <cmd>" — show help for specific command
        if command_name == "help" and args.prompt:
            topic = args.prompt[0]
            if topic == "slide" and len(args.prompt) > 1 and args.prompt[1] == "templates":
                sys.stderr.write(format_slide_help())
                return
            cmd = get_command(topic)
            if cmd:
                sys.stderr.write(format_command_help(cmd))
                return
            raise RuntimeError(f"unknown command: {topic}")
        print_usage()
        return

    if not args.prompt:
        print_usage()
        raise RuntimeError("no prompt provided")

    # Check for slide subtemplate: "slide funnel 'prompt'" -> subtemplate=funnel
    slide_template = None
    if command_name == "slide" and args.prompt:
        candidate = args.prompt[0]
        slide_template = get_slide_template(candidate)
        if slide_template:
            # Remove the subtemplate name from the prompt words
            args.prompt = args.prompt[1:]
            if not args.prompt:
                print_usage()
                raise RuntimeError("no prompt provided after slide subtemplate")

    user_prompt = " ".join(args.prompt)

    # Look up command (default to "generate" for free prompts)
    command = get_command(command_name) if command_name else None

    # Apply command defaults for aspect/size if user didn't set flags
    if command:
        effective_aspect_flag = args.aspect or command.default_aspect
        effective_size_flag = args.size or command.default_size
    else:
        effective_aspect_flag = args.aspect
        effective_size_flag = args.size

    # Load config file
    file_config = load_config()

    # Resolve configuration
    aspect, size, api_config = resolve_config(
        aspect_flag=effective_aspect_flag,
        size_flag=effective_size_flag,
        model_flag=args.model,
        file_config=file_config,
    )

    # Apply template to wrap the user prompt
    if slide_template:
        prompt = slide_template.template.format(user_prompt=user_prompt, size=size)
    elif command:
        prompt = command.apply(user_prompt, aspect=aspect, size=size)
    else:
        prompt = user_prompt

    print("Generating image...")
    if slide_template:
        print(f"  Command: slide ({slide_template.name})")
    elif command and command.name != "generate":
        print(f"  Command: {command.name}")
    print(f"  Prompt: {user_prompt}")
    if args.input_images:
        print(f"  Inputs: {', '.join(args.input_images)}")
    print(f"  Aspect: {aspect}")
    print(f"  Size:   {size}")
    if api_config.use_openrouter:
        print(f"  API:    OpenRouter ({api_config.model})")
    else:
        print("  API:    Gemini")

    # Generate image
    if api_config.use_openrouter:
        from nanobanana.openrouter import generate_image as gen_openrouter
        image_data, mime_type = gen_openrouter(
            api_key=api_config.api_key,
            model=api_config.model,
            prompt=prompt,
            input_images=args.input_images,
            aspect_ratio=aspect,
            image_size=size,
        )
    else:
        from nanobanana.gemini import generate_image as gen_gemini
        image_data, mime_type = gen_gemini(
            api_key=api_config.api_key,
            prompt=prompt,
            input_images=args.input_images,
            aspect_ratio=aspect,
            image_size=size,
        )

    # Determine output filename
    output_path = args.output
    correct_ext = extension_from_mime(mime_type)

    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"image_{timestamp}{correct_ext}"
    else:
        current_ext = Path(output_path).suffix.lower()
        if current_ext != correct_ext:
            output_path = str(Path(output_path).with_suffix("")) + correct_ext
            print(f"\nInfo: API returned {mime_type} format, adjusted output to: {output_path}")

    # Write file
    try:
        Path(output_path).write_bytes(image_data)
    except OSError as e:
        raise RuntimeError(f"failed to write output file: {e}") from e

    print(f"\nImage saved to: {output_path}")


def main() -> None:
    """Entry point that handles errors."""
    try:
        run()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
