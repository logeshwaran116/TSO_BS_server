from .handlers import send
from tools import playlist
import random

import _babase
import _bascenev1
import setting
from playersdata import pdata
# from tools.whitelist import add_to_white_list, add_commit_to_logs
from serverdata import serverdata

from stats import mystats

import babase
import bascenev1 as bs
from tools import logger


Commands = ['recents', 'info', 'createteam', 'showid', 'hideid', 'lm', 'gp',
            'party', 'quit', 'kickvote', 'maxplayers', 'playlist', 'ban',
            'kick', 'remove', 'end', 'quit', 'mute', 'unmute', 'slowmo', 'nv',
            'dv', 'pause', 'tint',
            'cameramode', 'createrole', 'addrole', 'removerole', 'addcommand',
            'addcmd', 'removecommand', 'getroles', 'removecmd', 'changetag',
            'customtag', 'customeffect', 'removeeffect', 'removetag', 'add',
            'spectators', 'lobbytime','acl']
CommandAliases = ['pme','max', 'rm', 'next', 'restart', 'mutechat', 'unmutechat',
                  'sm',
                  'slow', 'night', 'day', 'pausegame', 'camera_mode',
                  'rotate_camera', 'exchange','control', 'effect','say','hug','hugall','control','exchange','icy','cc','spaz','ccall','spazall','box','boxall','kickall','acl']


def ExcelCommand(command, arguments, clientid, accountid):
    """
    Checks The Command And Run Function

    Parameters:
        command : str
        arguments : str
        clientid : int
        accountid : int

    Returns:
        None
    """
    match command:
        case 'recents':
            get_recents(clientid)
        case 'info':
            get_player_info(arguments, clientid)
        case 'maxplayers' | 'max':
            changepartysize(arguments)
        case 'createteam':
            create_team(arguments)
        case 'playlist':
            changeplaylist(arguments)
        case 'kick':
            kick(arguments)
        case 'ban':
            ban(arguments)
        case 'end' | 'next':
            end(arguments)
        case 'kickvote':
            kikvote(arguments, clientid)
        case 'hideid':
            hide_player_spec()
        case 'showid':
            show_player_spec()
        case 'lm':
            last_msgs(clientid)
        case 'gp':
            get_profiles(arguments, clientid)
        case 'party':
            party_toggle(arguments)
        case 'quit' | 'restart':
            quit(arguments)
        case 'mute' | 'mutechat':
            mute(arguments,clientid)
        case 'unmute' | 'unmutechat':
            un_mute(arguments, clientid)
        case 'remove' | 'rm':
            remove(arguments)
        case 'sm' | 'slow' | 'slowmo':
            slow_motion()
        case 'control' | 'exchange':
            control(arguments, clientid)
        case 'nv' | 'night':
            nv(arguments)
        case 'tint':
            tint(arguments)
        case 'pause' | 'pausegame':
            pause()
        case 'cameraMode' | 'camera_mode' | 'rotate_camera':
            rotate_camera()
        case 'createrole':
            create_role(arguments)
        case 'addrole':
            add_role_to_player(arguments)
        case 'removerole':
            remove_role_from_player(arguments)
        case 'getroles':
            get_roles_of_player(arguments, clientid)
        case 'addcommand' | 'addcmd':
            add_command_to_role(arguments)
        case 'removecommand' | 'removecmd':
            remove_command_to_role(arguments)
        case 'changetag':
            change_role_tag(arguments)
        case 'customtag':
            set_custom_tag(arguments)
        case 'customeffect' | 'effect':
            set_custom_effect(arguments)
        case 'removetag':
            remove_custom_tag(arguments)
        case 'removeeffect':
            remove_custom_effect(arguments)
        case 'spectators':
            spectators(arguments)
        case 'lobbytime':
            change_lobby_check_time(arguments)
        case 'pme':
            stats_to_clientid(arguments, clientid, accountid)
        case 'say':
            server_chat(arguments, clientid)
        case 'hug':
            hug(arguments, clientid)
        case 'hugall':
            hugall(arguments, clientid)
        case 'icy':
            icy(arguments, clientid)
        case 'spaz' | 'cc':
            spaz(arguments, clientid)
        case 'ccall' | 'spazall':
            spazall(arguments, clientid)
        case 'box':
            box(arguments, clientid)
        case 'boxall':
            boxall(arguments, clientid)
        case 'kickall':
            kickall(arguments, clientid)
        case 'acl':
            acl(arguments, clientid)
        case 'control' | 'exchange':
            control(arguments, clientid)
        case _:
            pass





def control(arguments, clientid):
 activity = bs.get_foreground_host_activity()
 a = arguments
 with bs.Context(activity):
    try:
        if True:
            try:
                player1 = int(a[0])
            except:
                pass
            try:
                player2 = int(a[1])
            except:
                pass
        node1 = activity.players[player1].actor.node
        node2 = activity.players[player2].actor.node
        activity.players[player1].actor.node = node2
        activity.players[player2].actor.node = node1         
    except:
        send(f"Using: /exchange [PlayerID1] [PlayerID2]", clientid)



def spazall(arguments, clientid):
    activity = bs.get_foreground_host_activity()
    a = arguments
    with bs.Context(activity):
       for i in activity.players:
           try:
              if arguments != []:
                  appearance_name = a[0].lower()  # Convert to lowercase for case-insensitive comparison
                  valid_appearance_names = ['ali', 'wizard', 'cyborg', 'penguin', 'agent', 'pixie', 'bear', 'bunny']
                  # Check if the appearance name is valid
                  if appearance_name in valid_appearance_names:               
                      i.actor.node.color_texture = bs.gettexture(appearance_name + "Color")
                      i.actor.node.color_mask_texture = bs.gettexture(appearance_name + "ColorMask")
                      i.actor.node.head_model = bs.getmodel(appearance_name + "Head")
                      i.actor.node.torso_model = bs.getmodel(appearance_name + "Torso")
                      i.actor.node.pelvis_model = bs.getmodel(appearance_name + "Pelvis")
                      i.actor.node.upper_arm_model = bs.getmodel(appearance_name + "UpperArm")
                      i.actor.node.forearm_model = bs.getmodel(appearance_name + "ForeArm")
                      i.actor.node.hand_model = bs.getmodel(appearance_name + "Hand")
                      i.actor.node.upper_leg_model = bs.getmodel(appearance_name + "UpperLeg")
                      i.actor.node.lower_leg_model = bs.getmodel(appearance_name + "LowerLeg")
                      i.actor.node.toes_model = bs.getmodel(appearance_name + "Toes")
                      i.actor.node.style = appearance_name
                  else:
                      # If the appearance name is not valid, inform the user
                      send("Invalid CharacterName.\nPlease choose from: ali, wizard, cyborg, penguin, agent, pixie, bear, bunny", clientid)
              else:
                  send("Using: /spazall [CharacterName]", clientid)
           except Exception as e:
               print(f"Error in spaz command: {e}")
               send("An error occurred. Please try again.", clientid)


def spaz(arguments, clientid):
    activity = bs.get_foreground_host_activity()
    a = arguments
    with bs.Context(activity):
        try:
            if arguments != []:
                n = int(a[0])
                appearance_name = a[1].lower()  # Convert to lowercase for case-insensitive comparison
                valid_appearance_names = ['ali', 'wizard', 'cyborg', 'penguin', 'agent', 'pixie', 'bear', 'bunny']
                # Check if the appearance name is valid
                if appearance_name in valid_appearance_names:               
                    activity.players[n].actor.node.color_texture = bs.gettexture(appearance_name + "Color")
                    activity.players[n].actor.node.color_mask_texture = bs.gettexture(appearance_name + "ColorMask")
                    activity.players[n].actor.node.head_model = bs.getmodel(appearance_name + "Head")
                    activity.players[n].actor.node.torso_model = bs.getmodel(appearance_name + "Torso")
                    activity.players[n].actor.node.pelvis_model = bs.getmodel(appearance_name + "Pelvis")
                    activity.players[n].actor.node.upper_arm_model = bs.getmodel(appearance_name + "UpperArm")
                    activity.players[n].actor.node.forearm_model = bs.getmodel(appearance_name + "ForeArm")
                    activity.players[n].actor.node.hand_model = bs.getmodel(appearance_name + "Hand")
                    activity.players[n].actor.node.upper_leg_model = bs.getmodel(appearance_name + "UpperLeg")
                    activity.players[n].actor.node.lower_leg_model = bs.getmodel(appearance_name + "LowerLeg")
                    activity.players[n].actor.node.toes_model = bs.getmodel(appearance_name + "Toes")
                    activity.players[n].actor.node.style = appearance_name
                else:
                    # If the appearance name is not valid, inform the user
                    send("Invalid CharacterName.\nPlease choose from: ali, wizard, cyborg, penguin, agent, pixie, bear, bunny", clientid)
            else:
                send("Using: /spaz [PLAYER-ID] [CharacterName]", clientid)
        except Exception as e:
            print(f"Error in spaz command: {e}")
            send("An error occurred. Please try again.", clientid)



def box(arguments, clientid):
   activity = bs.get_foreground_host_activity()
   with bs.Context(activity):
    try:
        try:
            if arguments != []:
                n = int(arguments[0])      
            activity.players[n].actor.node.torso_model = bs.getmodel("tnt");
            activity.players[n].actor.node.color_mask_texture = bs.gettexture("tnt");
            activity.players[n].actor.node.color_texture = bs.gettexture("tnt") 
            activity.players[n].actor.node.highlight = (1,1,1)
            activity.players[n].actor.node.color = (1,1,1);
            activity.players[n].actor.node.head_model = None;
            activity.players[n].actor.node.style = "cyborg";
        except:
            send(f"Using: /boxall [or] /box [PlayerID]", clientid)
    except:
        send(f"Using: /boxall [or] /box [PlayerID]", clientid)

         #BOXALL
def boxall(arguments, clientid):
   activity = bs.get_foreground_host_activity()
   with bs.Context(activity):    
    try:
        for i in activity.players:
            try:
                i.actor.node.torso_model = bs.getmodel("tnt");
                i.actor.node.color_mask_texture = bs.gettexture("tnt");
                i.actor.node.color_texture = bs.gettexture("tnt")
                i.actor.node.highlight = (1,1,1);
                i.actor.node.color = (1,1,1);
                i.actor.node.head_model = None;
                i.actor.node.style = "cyborg";
            except:
                pass
    except:
        pass


def hug(arguments, clientid):
    activity = bs.get_foreground_host_activity()
    if arguments == [] or arguments == ['']:
     with bs.Context(activity):
        send(f"Using: /hugall [or] /hug [player1Index] [player2Index]", clientid)
    else:
        try:
            activity.players[int(arguments[0])].actor.node.hold_node = activity.players[int(arguments[1])].actor.node
        except:
            pass
            
            
def hugall(arguments, clientid):
    activity = bs.get_foreground_host_activity()
    with bs.Context(activity):    
     try:
         activity.players[0].actor.node.hold_node = activity.players[1].actor.node
     except:
         pass
     try:
         activity.players[1].actor.node.hold_node = activity.players[0].actor.node
     except:
         pass
     try:
         activity.players[2].actor.node.hold_node = activity.players[3].actor.node
     except:
         pass
     try:
         activity.players[3].actor.node.hold_node = activity.players[2].actor.node
     except:
         pass
     try:
          activity.players[4].actor.node.hold_node = activity.players[5].actor.node
     except:
         pass
     try:
         activity.players[5].actor.node.hold_node = activity.players[4].actor.node
     except:
         pass
     try:
         activity.players[6].actor.node.hold_node = activity.players[7].actor.node
     except:
         pass
     try:
         activity.players[7].actor.node.hold_node = activity.players[6].actor.node
     except:
         pass

#KICK ALL :)))))))))        
def kickall(arguments, clientid):
    try:
        for i in bs.get_game_roster():
            if i['client_id'] != clientid:
                bs.disconnect_client(i['client_id'])
    except:
        pass


def server_chat(arguments, clientid):
    if arguments == []:
        bs.broadcastmessage('Usage: /say <text to send>', transient=True, clients=[clientid])
    else:
        message = " ".join(arguments)
        bs.chatmessage(message)


def stats_to_clientid(arguments, clid, acid):
     activity = bs.get_foreground_host_activity()
     if arguments == [] or arguments == ['']:
        with bs.Context(activity):
         send(f"Using: /pme [Clientid of player]", clid)
     else:
         cl_id = int(arguments[0])
         for pla in bs.get_foreground_host_session().sessionplayers:
              if pla.inputdevice.client_id == cl_id:
                 fname = pla.getname(full=True, icon=True)
         for roe in bs.get_game_roster():
              if roe["client_id"] == cl_id:
                 pbid = roe["account_id"]
                 stats = mystats.get_stats_by_id(pbid)  
                 if stats:
                     reply = (
                         f"\ue048| Name: {fname}\n"
                         f"\ue048| PB-ID: {stats['aid']}\n"
                         f"\ue048| Rank: {stats['rank']}\n"
                         f"\ue048| Score: {stats['scores']}\n"
                         f"\ue048| Games: {stats['games']}\n"
                         f"\ue048| Kills: {stats['kills']}\n"
                         f"\ue048| Deaths: {stats['deaths']}\n"
                         f"\ue048| Avg.: {stats['avg_score']}\n"
                     )
                     send(reply, clid)
                 else:
                     areply = "Not played any match yet."
                     send(areply, clid)


def create_team(arguments):
    if len(arguments) == 0:
        bs.chatmessage("enter team name")
    else:
        from bascenev1._team import SessionTeam
        bs.get_foreground_host_session().sessionteams.append(SessionTeam(
            team_id=len(bs.get_foreground_host_session().sessionteams) + 1,
            name=str(arguments[0]),
            color=(random.uniform(0, 1.2), random.uniform(
                0, 1.2), random.uniform(0, 1.2))))
        from bascenev1._lobby import Lobby
        bs.get_foreground_host_session().lobby = Lobby()


def hide_player_spec():
    _babase.hide_player_device_id(True)


def show_player_spec():
    _babase.hide_player_device_id(False)


def get_player_info(arguments, client_id):
    if len(arguments) == 0:
        send("invalid client id", client_id)
    for account in serverdata.recents:
        if account['client_id'] == int(arguments[0]):
            send(pdata.get_detailed_info(account["pbid"]), client_id)


def get_recents(client_id):
    for players in serverdata.recents:
        send(
            f"{players['client_id']} {players['deviceId']} {players['pbid']}",
            client_id)


def changepartysize(arguments):
    if len(arguments) == 0:
        bs.chatmessage("enter number")
    else:
        bs.set_public_party_max_size(int(arguments[0]))


def changeplaylist(arguments):
    if len(arguments) == 0:
        bs.chatmessage("enter list code or name")
    else:
        if arguments[0] == 'coop':
            serverdata.coopmode = True
        else:
            serverdata.coopmode = False
        playlist.setPlaylist(arguments[0])
    return


def kick(arguments):
    cl_id = int(arguments[0])
    for ros in bs.get_game_roster():
        if ros["client_id"] == cl_id:
            try:
                if pdata.is_protected(ros.get('account_id')):
                    send("Cannot kick a protected player", cl_id)
                    return
            except Exception:
                pass
            logger.log("kicked " + ros["display_string"])
    bs.disconnect_client(int(arguments[0]))
    return


def kikvote(arguments, clientid):
    if arguments == [] or arguments == [''] or len(arguments) < 2:
        return

    elif arguments[0] == 'enable':
        if arguments[1] == 'all':
            _babase.set_enable_default_kick_voting(True)
        else:
            try:
                cl_id = int(arguments[1])
                for ros in bs.get_game_roster():
                    if ros["client_id"] == cl_id:
                        pdata.enable_kick_vote(ros["account_id"])
                        logger.log(
                            f'kick vote enabled for {ros["account_id"]} {ros["display_string"]}')
                        send(
                            "Upon server restart, Kick-vote will be enabled for this person",
                            clientid)
                return
            except:
                return

    elif arguments[0] == 'disable':
        if arguments[1] == 'all':
            _babase.set_enable_default_kick_voting(False)
        else:
            try:
                cl_id = int(arguments[1])
                for ros in bs.get_game_roster():
                    if ros["client_id"] == cl_id:
                        _bascenev1.disable_kickvote(ros["account_id"])
                        send("Kick-vote disabled for this person", clientid)
                        logger.log(
                            f'kick vote disabled for {ros["account_id"]} {ros["display_string"]}')
                        pdata.disable_kick_vote(
                            ros["account_id"], 2, "by chat command")
                return
            except:
                return
    else:
        return


def last_msgs(clientid):
    for i in bs.get_chat_messages():
        send(i, clientid)


def get_profiles(arguments, clientid):
    try:
        playerID = int(arguments[0])
        num = 1
        for i in bs.get_foreground_host_session().sessionplayers[
                playerID].inputdevice.get_player_profiles():
            try:
                send(f"{num})-  {i}", clientid)
                num += 1
            except:
                pass
    except:
        pass


def party_toggle(arguments):
    if arguments == ['public']:
        bs.set_public_party_enabled(True)
        bs.chatmessage("party is public now")
    elif arguments == ['private']:
        bs.set_public_party_enabled(False)
        bs.chatmessage("party is private now")
    else:
        pass


def end(arguments):
    if arguments == [] or arguments == ['']:
        try:
            game = bs.get_foreground_host_activity()
            with game.context:
                game.end_game()
        except:
            pass


def ban(arguments):
    try:
        cl_id = int(arguments[0])
        duration = int(arguments[1]) if len(arguments) >= 2 else 0.5
        for ros in bs.get_game_roster():
            if ros["client_id"] == cl_id:
                pdata.ban_player(ros['account_id'], duration,
                                 "by chat command")
                logger.log(f'banned {ros["display_string"]} by chat command')

        for account in serverdata.recents:  # backup case if player left the server
            if account['client_id'] == int(arguments[0]):
                pdata.ban_player(
                    account["pbid"], duration, "by chat command")
                logger.log(
                    f'banned {account["pbid"]} by chat command, recents')
        kick(arguments)
    except:
        pass


def quit(arguments):
    if arguments == [] or arguments == ['']:
        babase.quit()


def mute(arguments, clientid):
    if len(arguments) == 0:
        serverdata.muted = True
        bs.chatmessage("Global chat mute enabled")
        logger.log("Server muted by chat command")
        return
    
    try:
        cl_id = int(arguments[0])
        duration = int(arguments[1]) if len(arguments) >= 2 else 0.5

        for me in bs.get_game_roster():
            if me["client_id"] == clientid:
                myself = me["display_string"]

        player_name = "Unknown Player"
        
        # Find player name from game roster
        for ros in bs.get_game_roster():
            if ros["client_id"] == cl_id:
                player_name = ros["display_string"]
                ac_id = ros['account_id']
                logger.log(f'muted {player_name}')
                pdata.mute(ac_id, duration, "muted by chat command")
                bs.chatmessage(f"{myself} muted {player_name} for {duration} days")
                return
        
        # Backup case if player left the server - try to get name from recents
        for account in serverdata.recents:
            if account['client_id'] == cl_id:
                player_name = account.get('name', 'Unknown Player')
                pdata.mute(account["pbid"], duration, "muted by chat command, from recents")
                bs.chatmessage(f"{player_name} is muted for {duration} hours (from recents)")
                return
                
        bs.chatmessage(f"Player with client ID {cl_id} not found")
        
    except ValueError:
        bs.chatmessage("Invalid arguments. Usage: /mute [client_id] [duration_hours]")
    except Exception as e:
        logger.log(f"Error in mute command: {e}")
        bs.chatmessage("An error occurred while muting the player")


def un_mute(arguments, clientid):
    if len(arguments) == 0:
        serverdata.muted = False
        logger.log("Server unmuted by chat command")
        bs.chatmessage("Global chat mute disabled")
        return
    
    try:
        cl_id = int(arguments[0])

        for me in bs.get_game_roster():
            if me["client_id"] == clientid:
                myself = me["display_string"]

        player_name = "Unknown Player"
        
        # Find player name from game roster
        for ros in bs.get_game_roster():
            if ros["client_id"] == cl_id:
                player_name = ros["display_string"]
                pdata.unmute(ros['account_id'])
                logger.log(f'unmuted {player_name} by chat command')
                bs.chatmessage(f"{myself} unmuted {player_name}")
                return
        
        # Backup case if player left the server
        for account in serverdata.recents:
            if account['client_id'] == cl_id:
                player_name = account.get('name', 'Unknown Player')
                pdata.unmute(account["pbid"])
                logger.log(f'unmuted {player_name} by chat command, recents')
                bs.chatmessage(f"{myself} unmuted {player_name} is unmuted (from recents)")
                return
                
        bs.chatmessage(f"Player with client ID {cl_id} not found")
        
    except ValueError:
        bs.chatmessage("Invalid arguments. Usage: /unmute [client_id]")
    except Exception as e:
        logger.log(f"Error in unmute command: {e}")
        bs.chatmessage("An error occurred while unmuting the player")

def remove(arguments):
    if arguments == [] or arguments == ['']:
        return

    elif arguments[0] == 'all':
        session = bs.get_foreground_host_session()
        for i in session.sessionplayers:
            i.remove_from_game()

    else:
        try:
            session = bs.get_foreground_host_session()
            for i in session.sessionplayers:
                if i.inputdevice.client_id == int(arguments[0]):
                    i.remove_from_game()
        except:
            return


def slow_motion():
    activity = bs.get_foreground_host_activity()

    if not activity.globalsnode.slow_motion:
        activity.globalsnode.slow_motion = True

    else:
        activity.globalsnode.slow_motion = False


def nv(arguments):
    def is_close(a, b, tol=1e-5):
        return all(abs(x - y) < tol for x, y in zip(a, b))

    try:
        activity = bs.get_foreground_host_activity()
        nv_tint = (0.5, 0.5, 1.0)
        nv_ambient = (1.5, 1.5, 1.5)
        
        if is_close(activity.globalsnode.tint, nv_tint):
            activity.globalsnode.tint = (1, 1, 1)
            #adding ambient color to imitate moonlight reflection on objects
            activity.globalsnode.ambient_color = (1, 1, 1)
            #print(activity.globalsnode.tint)
        else:
            activity.globalsnode.tint = nv_tint
            activity.globalsnode.ambient_color = nv_ambient
            #print(activity.globalsnode.tint)
    except:
        return


def tint(arguments):
    
    if len(arguments) == 3:
        args = arguments
        r, g, b = float(args[0]), float(args[1]), float(args[2])
        try:
            # print(dir(activity.globalsnode))
            
            activity = bs.get_foreground_host_activity()
            activity.globalsnode.tint = (r, g, b)
        except:
            return


def pause():
    activity = bs.get_foreground_host_activity()

    if not activity.globalsnode.paused:
        activity.globalsnode.paused = True

    else:
        activity.globalsnode.paused = False


def rotate_camera():
    activity = _babase.get_foreground_host_activity()

    if activity.globalsnode.camera_mode != 'rotate':
        activity.globalsnode.camera_mode = 'rotate'

    else:
        activity.globalsnode.camera_mode = 'normal'


def create_role(arguments):
    try:
        pdata.create_role(arguments[0])
    except:
        return


def add_role_to_player(arguments):
    try:

        session = bs.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                roles = pdata.add_player_role(
                    arguments[0], i.get_v1_account_id())
    except:
        return


def remove_role_from_player(arguments):
    try:
        session = bs.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                roles = pdata.remove_player_role(
                    arguments[0], i.get_v1_account_id())

    except:
        return


def get_roles_of_player(arguments, clientid):
    try:
        session = bs.get_foreground_host_session()
        roles = []
        reply = ""
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[0]):
                roles = pdata.get_player_roles(i.get_v1_account_id())

        for role in roles:
            reply = reply + role + ","
        send(reply, clientid)
    except:
        return


def change_role_tag(arguments):
    try:
        pdata.change_role_tag(arguments[0], arguments[1])
    except:
        return


def set_custom_tag(arguments):
    try:
        session = bs.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                roles = pdata.set_tag(arguments[0], i.get_v1_account_id())
    except:
        return


def remove_custom_tag(arguments):
    try:
        session = bs.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[0]):
                pdata.remove_tag(i.get_v1_account_id())
    except:
        return


def remove_custom_effect(arguments):
    try:
        session = bs.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[0]):
                pdata.remove_effect(i.get_v1_account_id())
    except:
        return


def set_custom_effect(arguments):
    try:
        session = bs.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                pdata.set_effect(arguments[0], i.get_v1_account_id())
    except:
        return


all_commands = ["changetag", "createrole", "addrole", "removerole",
                "addcommand", "addcmd", "removecommand", "removecmd", "kick",
                "remove", "rm", "end", "next", "quit", "restart", "mute",
                "mutechat", "unmute", "unmutechat", "sm", "slow", "slowmo",
                "nv", "night", "dv", "day", "pause", "pausegame", "cameraMode",
                "camera_mode", "rotate_camera", "kill", "die", "heal", "heath",
                "curse", "cur", "sleep", "sp", "superpunch", "gloves", "punch",
                "shield", "protect", "freeze", "ice", "unfreeze", "thaw", "gm",
                "godmode", "fly", "inv", "invisible", "hl", "headless",
                "creepy", "creep", "celebrate", "celeb", "spaz","pme","say","hug","hugall","cc","spaz"
                "ccall","spazall","acl","control","exchange","icy","box","boxall","kickall"]


def add_command_to_role(arguments):
    try:
        if len(arguments) == 2:
            pdata.add_command_role(arguments[0], arguments[1])
        else:
            bs.chatmessage("invalid command arguments")
    except:
        return


def remove_command_to_role(arguments):
    try:
        if len(arguments) == 2:
            pdata.remove_command_role(arguments[0], arguments[1])
    except:
        return


# def whitelst_it(accountid : str, arguments):
#     settings = setting.get_settings_data()

#     if arguments[0] == 'on':
#         if settings["white_list"]["whitelist_on"]:
#             bs.chatmessage("Already on")
#         else:
#             settings["white_list"]["whitelist_on"] = True
#             setting.commit(settings)
#             bs.chatmessage("whitelist on")
#             from tools import whitelist
#             whitelist.Whitelist()
#         return

#     elif arguments[0] == 'off':
#         settings["white_list"]["whitelist_on"] = False
#         setting.commit(settings)
#         bs.chatmessage("whitelist off")
#         return

# else:
#     rost = bs.get_game_roster()

#     for i in rost:
#         if i['client_id'] == int(arguments[0]):
#             add_to_white_list(i['account_id'], i['display_string'])
#             bs.chatmessage(str(i['display_string'])+" whitelisted")
#             add_commit_to_logs(accountid+" added "+i['account_id'])


def spectators(arguments):
    if arguments[0] in ['on', 'off']:
        settings = setting.get_settings_data()

        if arguments[0] == 'on':
            settings["white_list"]["spectators"] = True
            setting.commit(settings)
            bs.chatmessage("spectators on")

        elif arguments[0] == 'off':
            settings["white_list"]["spectators"] = False
            setting.commit(settings)
            bs.chatmessage("spectators off")


def change_lobby_check_time(arguments):
    try:
        argument = int(arguments[0])
    except:
        bs.chatmessage("must type number to change lobby check time")
        return
    settings = setting.get_settings_data()
    settings["white_list"]["lobbychecktime"] = argument
    setting.commit(settings)
    bs.chatmessage(f"lobby check time is {argument} now")