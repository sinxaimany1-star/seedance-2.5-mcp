from __future__ import annotations

import os
from typing import Optional

from mcp.server.fastmcp import FastMCP

from server_core import execute_tool, api_key_from_env


mcp = FastMCP(
    "Seedance 2.5",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def seedance_25_text_to_video(
    prompt: str,
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
    duration: int = 5,
    seed: int = -1,
):
    """Generate a Seedance 2.5 video from text."""
    return execute_tool(
        "seedance_25_text_to_video",
        {
            "prompt": prompt,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "seed": seed,
        },
        api_key_from_env(),
        wait=True,
    )


@mcp.tool()
def seedance_25_image_to_video(
    prompt: str,
    image_url: str,
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
    duration: int = 5,
    seed: int = -1,
):
    """Animate an image with Seedance 2.5."""
    return execute_tool(
        "seedance_25_image_to_video",
        {
            "prompt": prompt,
            "image_url": image_url,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "seed": seed,
        },
        api_key_from_env(),
        wait=True,
    )


@mcp.tool()
def seedance_25_first_last_frame(
    prompt: str,
    images_list: list[str],
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
    duration: int = 5,
    seed: int = -1,
):
    """Generate a transition between first and last frame."""
    return execute_tool(
        "seedance_25_first_last_frame",
        {
            "prompt": prompt,
            "images_list": images_list,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "seed": seed,
        },
        api_key_from_env(),
        wait=True,
    )


@mcp.tool()
def seedance_25_omni_reference(
    prompt: str,
    images_list: Optional[list[str]] = None,
    videos_list: Optional[list[str]] = None,
    audios_list: Optional[list[str]] = None,
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
    duration: int = 5,
    seed: int = -1,
):
    """Generate a video using image, video, or audio references."""
    args = {
        "prompt": prompt,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
        "seed": seed,
    }

    if images_list:
        args["images_list"] = images_list
    if videos_list:
        args["videos_list"] = videos_list
    if audios_list:
        args["audios_list"] = audios_list

    return execute_tool(
        "seedance_25_omni_reference",
        args,
        api_key_from_env(),
        wait=True,
    )


@mcp.tool()
def muapi_predict_result(request_id: str):
    """Get a MuAPI prediction result."""
    return execute_tool(
        "muapi_predict_result",
        {"request_id": request_id},
        api_key_from_env(),
        wait=True,
    )


@mcp.tool()
def muapi_account_balance():
    """Check MuAPI account balance."""
    return execute_tool(
        "muapi_account_balance",
        {},
        api_key_from_env(),
        wait=True,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        streamable_http_path="/mcp",
    )
