import json
import subprocess
from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path

import project_setup

DEFAULT_PAYLOAD = json.dumps(
    [
        {
            "version_code": "",
            "spawn_rate": 10,
        }
    ]
)


def build_parser() -> ArgumentParser:
    parser = project_setup.build_parser()
    payload_group = parser.add_mutually_exclusive_group()
    payload_group.add_argument(
        "--payload",
        required=False,
        help="JSON payload to pass to the Godot build script.",
    )
    payload_group.add_argument(
        "--payload-file",
        required=False,
        help="Path to a JSON file containing the payload.",
    )
    return parser


def _validate_payload(payload: str) -> None:
    if payload is None or payload == "":
        raise ValueError("Payload is not set.")

    try:
        loaded_payload = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Payload is not valid JSON: {exc}") from exc

    if not isinstance(loaded_payload, list):
        raise ValueError("Payload must be a JSON array.")
    if len(loaded_payload) == 0:
        raise ValueError("Payload array is empty.")
    if not isinstance(loaded_payload[0], dict):
        raise ValueError("Payload items must be JSON objects.")

    spawn_rate = loaded_payload[0].get("spawn_rate")
    if spawn_rate is None:
        raise ValueError("Payload spawn_rate is required.")
    if not isinstance(spawn_rate, (int, float)):
        raise ValueError("Payload spawn_rate must be a number.")
    if spawn_rate < 0:
        raise ValueError("Payload spawn_rate must be non-negative.")


def _load_payload(args: Namespace) -> str:
    if args.payload_file:
        payload_path = Path(args.payload_file)
        if not payload_path.exists():
            raise ValueError(f"Payload file does not exist: {payload_path}")
        payload = payload_path.read_text(encoding="utf-8")
    elif args.payload:
        payload = args.payload
    else:
        payload = environ.get("BUILD_PAYLOAD", DEFAULT_PAYLOAD)

    _validate_payload(payload)
    return payload


def build_command(setup: project_setup.ProjectSetup, payload: str) -> list[str]:
    output_path = setup.build_output_path / setup.exported_project_name
    return [
        setup.godot_editor_path,
        "--headless",
        "--path",
        str(setup.your_project_path),
        "-s",
        setup.script_path,
        "--export-debug",
        setup.exported_platform,
        str(output_path),
        "--",
        payload,
    ]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        setup = project_setup.prepare_setup(args)
        payload = _load_payload(args)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    command = build_command(setup, payload)

    print("Running build command:")
    print("Command:", command)

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"Failed to launch Godot editor. Return code: {result.returncode}")
        return result.returncode

    print("Build preparation step completed!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
