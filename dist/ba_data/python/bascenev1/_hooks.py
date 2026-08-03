# Released under the MIT License. See LICENSE for details.
#
"""Snippets of code for use by the c++ layer."""
# (most of these are self-explanatory)
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
import _bascenev1
from playersdata import  pdata

if TYPE_CHECKING:
    from typing import Any

    import bascenev1


def launch_main_menu_session() -> None:
    assert babase.app.classic is not None

    _bascenev1.new_host_session(babase.app.classic.get_main_menu_session())


def get_player_icon(sessionplayer: bascenev1.SessionPlayer) -> dict[str, Any]:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }

def filter_chat_message(msg: str, client_id: int) -> str | None:
    try:
        import custom_hooks as chooks
    except:
        pass
    """Intercept/filter chat messages.

    Called for all chat messages while hosting.
    Messages originating from the host will have clientID -1.
    Should filter and return the string to be displayed, or return None
    to ignore the message.
    """
    try:
        return chooks.filter_chat_message(msg,client_id)
    except:
        return msg

    
import traceback

def kick_vote_started(by: str, to: str) -> None:
    print("kick vote started by " + by + " to " + to)
    by = by.strip('"').strip("'")
    to = to.strip('"').strip("'")

    print(f"[DEBUG] {by} started kick vote for {to}.")

    try:
        roles = pdata.get_roles()
        immune_roles = ("protected", "owner", "moderator", "leadstaff")

        for role_name in immune_roles:
            if role_name in roles and to in roles[role_name].get("ids", []):
                print(f"[DEBUG] {to} found in role '{role_name}' → immune")

                session = bs.get_foreground_host_session()
                if session is not None:
                    with session.context:
                        _bascenev1.set_enable_default_kick_voting(False)
                        print("[DEBUG] Disabled default kick voting")

                        def _reenable():
                            try:
                                _bascenev1.set_enable_default_kick_voting(True)
                                print("[DEBUG] Re-enabled default kick voting")
                            except Exception:
                                traceback.print_exc()

                        bs.timer(30.0, babase.Call(_reenable))
                break
    except Exception as e:
        print(f"[DEBUG] Exception occurred: {e}")
        traceback.print_exc()


def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = (
        None if classic.party_window is None else classic.party_window()
    )

    if party_window is not None:
        party_window.on_chat_message(msg)
