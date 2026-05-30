# ba_meta require api 9
# Copyright 2025 - Mod Created by BrotherBoard
# Modified with extra skills & all-map support
# Added by Sara
"""
Ender v1.0 - You're done.

A deadly bot that actively hunts any spaz nodes.
I wrote some cool pvp abilities into its core.
It spawns at a random player's location or at the center if no players are present.
Occasionally uses bubble_min to talk based on situations.

To spawn, just call Ender from dev console:
>>> __import__('ender').Ender()
To spawn, just call Ender in on_beigin() def (for server)
>>> import Ender
>>> Ender.enable()
Tested in football stadium. Read code to know more.
"""

from bascenev1lib.actor.spaz import Spaz
from babase import (
    get_string_height as gsh,
    get_string_width as gsw,
    Plugin
)
import babase
import bascenev1 as bs
from bascenev1 import (
    get_foreground_host_activity as ga,
    OutOfBoundsMessage,
    getnodes as GN,
    timer as tick,
    Timer as tock,
    StandMessage,
    DieMessage,
    newnode,
    animate,
    time
)
from math import dist, sqrt
from random import choice, random
from bascenev1 import get_foreground_host_activity, getnodes, timer

#============== BOT NAME =================#
BOTNAME = "Makima" 
#===========================================#

class Bot:
    """
    The base class for all bot types.
    
    This class provides the fundamental functionality for a bot, including:
    - Initializing the Spaz actor and its associated node.
    - Creating a speech bubble for text display.
    - Methods for basic actions like waving, jumping, punching, picking up,
      and running.
    - Methods to control movement on the x and z axes.
    """
    def __init__(
        s,
        position: tuple = (0,0,0),
        color: tuple = (0.914, 0.902, 0.839),
        highlight: tuple = (0.827, 0.592, 0.561),
        character: str = 'Pixel'
    ):
        activity = bs.get_foreground_host_activity()
        # Get enemy team safely
        enemy_team = None
        if activity and len(activity.teams) > 1:
            enemy_team = activity.teams[1]
        s.bot = Spaz(
            color=color,
            highlight=highlight,
            character=character,
            source_player=None
        )
        # 🔥 Assign team properly
        if enemy_team:
            s.bot._team = enemy_team
            s.bot.team = enemy_team
        if ENABLE_GLOVES:
            s.bot.equip_boxing_gloves()
        # Equip shield if enabled
        if ENABLE_SHIELD:
            s.bot.equip_shields()        
        s.bot.handlemessage(StandMessage(position,0))
        s.node = s.bot.node
        s.node.name = s.__class__.__name__
        s.bub = Bubble(s.node)
    def wave(s):
        s.node.handlemessage('celebrate_r',1000)
    def on(s,i):
        for _ in [1,0]:
            getattr(s.bot,'on_'+['jump','bomb','pickup','punch'][i]+'_'+['release','press'][_])()
    def on_run(s, v: int):
        """New method to toggle running."""
        s.bot.on_run(v)
    def move(s,x,z):
        s.bot.on_move_left_right(x)
        s.bot.on_move_up_down(z)

class Bubble:
    """
    A class to create a speech bubble floating above a node.
    
    This bubble displays text and can be animated to appear and disappear.
    It consists of a background text block and a foreground text block
    to create a solid look.
    """
    def __init__(s,head,res='\u2588',resw=19.0):
        s.head = head
        s.res = res
        s.resw = resw
        s.text = ''
        s.kids = []
        s.bye = None
        s.node = newnode(
            'math',
            delegate=s,
            attrs={
                'input1':(0,0,0),
                'operation':'add'
            }
        )
        head.connectattr('position',s.node,'input2')
        for _ in [0,0.85]:
            n = TEX(s.node,color=(_,_,_))
            s.kids.append(n)
            s.node.connectattr('output',n,'position')
    def push(s,text=''):
        s.bye = None
        if not text: s.anim(1,0); s.text = text; return
        ls = len(text.splitlines())
        s.node.input1 = (0,1.3+0.32*ls,0)
        bg,t = s.kids
        bg.text = (round(GSW(text)/s.resw+1)*s.res+'\n')*ls
        t.text = text
        if not s.text: s.anim(0,1)
        s.text = text
        s.bye = tock(3.5,s.push)
    def anim(s,p1,p2):
        try:
            [animate(_,'opacity',{0:p1,0.2:p2}) for _ in s.kids]
        except:
            pass

class Ender(Bot):
    """
    The main AI bot class.
    
    This bot actively seeks out and attacks other players. Its AI is built on a
    fast-acting protective thread for immediate reactions and a slower main
    thinking loop for strategic decisions. It has several distinct behaviors:
    - Spawning: The bot spawns at a random player's location or at the
      center of the map if there are no players.
    - Combat: It uses a punch-grab combo when a target is in close proximity.
    - Messaging: It "talks" using a speech bubble, with specific messages for
      pursuing a target, acquiring it, releasing it, or being left alone.
    - Urgent Message: The "Don't hold me!" message has top priority and
      can be triggered even if a normal message cooldown is active.
    """
    def __init__(
        s,
        position: tuple = None, # Position is now None by default
        color: tuple = (0, 0, 0), # Color is now black
        highlight: tuple = (0, 0, 0),
        character: str = 'Pixel',
        name: str = None
    ):
        # Determine spawn position based on the presence of other players
        player_nodes = [
            n for n in GN() if n.exists() and n.getnodetype() == 'spaz'
        ]
        
        if not player_nodes:
            # If no players, spawn at (0, 0.1, 0)
            initial_position = (0, 0.1, 0)
        else:
            # If players exist, spawn at a random one's position
            target_node = choice(player_nodes)
            initial_position = target_node.position
            
        # Call the parent class constructor with the determined position
        super().__init__(initial_position, color, highlight, character)
        s.node.name = name if name else s.__class__.__name__  # Set the name

        s.last_skill_time = 0.0 # Cooldown for skill2
        s.speech_cooldown = 1.5 # Cooldown for messages
        s.last_speech_time = 0.0
        s.last_idle_chat_time = 0.0 # New cooldown for idle messages
        s.last_held_message_time = 0.0 # New cooldown for held messages
        s.held_message_cooldown = 1.0 # The "irreplaceable" message cooldown
        
        # Main think timer for general strategy (slower)
        s._think_timer = tock(0.15, s._think, repeat=True)

        # Protective thread for fast, defensive reactions
        s._protective_timer = tock(0.001, s._protective_think, repeat=True)

        s.is_shaking = False
        s._skill1_timer = None
        s._shake_timer = None
        
        # New state variable to prevent message spam
        s._has_announced_target = False

        # Greed messages
        s.greed_messages = [
            'Ippo dhaan en neram aarambam',
            'Inimey aatam vera maari irukkum',
            'Power vandhuruchu da',
            'Level up aayiten',
            'Ippo yaaru stop panna pora?',
            'Ketta payyan sir indha Kaali',
            'Naan oru thadava strong aana mudinjiduchu',
            'Idhu vera level upgrade',
            'Inimey damage adhigam',
            'Ippo dhaan full form ku vandhen',
            'Kingu maker vandhutan',
            'En vazhi thani vazhi da',
            'Mass mode activated',
            'Inimey adhiradi dhaan',
            'Neruppu da, touch panna sudum',
            'Ippo game en kai la',
            'Power ah paathu bayandhudu',
            'Vandhuten nu sollu, thirumbi vandhuten nu sollu',
            'Singam single ah dhaan varum',
            'Scene ah maathidalam va'
        ]

        # Funny messages
        s.pursuit_messages = [
            'Oduda, mudinja alavuku oduda',
            'Un game mudinjiduchu da',
            'Unna thedi vandhuten',
            'Ippo nee en target',
            'Kandupidichiten da',
            'Enga odinalum naan varuven',
            'Un location en kai la',
            'Inimey escape illa',
            'Nee maatikitta da',
            'Unakku sangu dhaan',
            'Neram vandhuruchu',
            'Un chapter close panna poren',
            'Kanna vechu paathuten',
            'Ippo yaaru kaapathuva?',
            'Vettaikaran vandhutan',
            'Un pinadi dhaan irukken',
            'Bayam irukka? Irukkanum',
            'Thappika chance romba kammi',
            'Catch panniten da',
            'Oduradhu thavira vera vazhi illa'
        ]

        s.acquire_messages = [
            'Avlodhan, close panniten',
            'Mudichu vechiten da',
            'Kathai mudinjudhu',
            'Game over da',
            'Target clear',
            'Velai mudinjudhu',
            'Mission successful',
            'Nee out da',
            'Sangu oodhiten',
            'Anuppi vechiten',
            'Adichu mudichiten',
            'List la irundhu remove panniten',
            'Ticket confirm aayiduchu',
            'Poi serndhutaan',
            'One shot, total damage',
            'Climax mudinjudhu',
            'Innoruthan count aayitaan',
            'Mark pannadhu mudichiten',
            'Setha payale',
            'Next yaaru?'
        ]

        s.release_messages = [
            'Velai mudinjudhu, kilambalam',
            'Case closed',
            'Chapter close panniyachu',
            'Mission complete',
            'Kanakku settle',
            'Target history aayitaan',
            'File close panniten',
            'Aattam mudinjudhu',
            'Account clear',
            'Work complete',
            'Mark remove panniyachu',
            'Neram mudinjudhu',
            'Poi serndhutaan',
            'Velaiya suthama mudichiten',
            'List update pannunga',
            'Contract complete',
            'Inga namma velai mudinjudhu',
            'Next assignment ready',
            'Mudichitu varen nu sonnenla',
            'Next yaaru?'
        ]

        s.idle_messages = [
            'Yaarume illaya da inge?',
            'Ellarum enga poitaanga?',
            'Server la kaathu dhaan varudhu',
            'Oru payalum kaanom',
            'Naanum waiting, neeyum waiting',
            'Vera yaaravadhu vaangada',
            'Indha amaidhi romba dangerous ah irukku',
            'Scene eh illa da',
            'Server ah lock pannitanga pola',
            'Enna koduma sir idhu',
            'Naan thaniya enna pannuradhu?',
            'Ghost server ah maari irukku',
            'Vandhavanum poitaan',
            'Online la yaarume illaya?',
            'Population: poojyam',
            'Echo... echo... echo...',
            'Aattam poda aal venum da',
            'Target kidaikala pa',
            'Match start panna aal thevai',
            'Server ku drishti suthanum pola',
            'Amaidhiye bayama irukku',
            'Naan ready, makkal enga?',
            'Inga naanum kaathum dhaan',
            'Waiting for player 1...',
            'Solo ah irukkuradhu bore adikudhu',
            'Lobby vida sudukadu busy ah irukku',
            'Yaaravadhu join pannunga da',
            'Refresh panninaalum yaarum varala',
            'Adutha entry eppo?',
            'Server ku uyir kodunga da'
        ]


        s.held_messages = [
            'Enna pudichadhu periya thappu da',
            'Thappana aala pudichita',
            'Kai vechadhe un thappu',
            'En mela kaiya vechitiya?',
            'Nee maatikitta da',
            'Pudichadhaala jeyikka mudiyadhu',
            'Kaiya vidra illa na kashtam',
            'Enna control panna mudiyadhu da',
            'Neruppa pudicha maari irukku',
            'Un kai dhaan mudhala pogum',
            'Pudichitu enna pannuva?',
            'Bayam illama kai vechitiya',
            'Kaiya vecha udane un kadhai mudinjudhu',
            'Ippo idhu personal da',
            'Singatha vaala pudicha maari pannita',
            'Setha payale, kaiya vidu',
            'Unakku thairiyam jaasthi da',
            'Kaiya vechadhukku bill varum',
            'Touch pannadhe thappu',
            'Ippo nee escape aaga mudiyadhu'
        ]

    def _say(s, message: str):
        """Handles speaking with a cooldown to prevent spam."""
        now = time()
        if now - s.last_speech_time > s.speech_cooldown:
            s.bub.push(message)
            s.last_speech_time = now

    def _say_held(s):
        """Urgent message with its own cooldown, overriding normal speech."""
        now = time()
        if now - s.last_held_message_time > s.held_message_cooldown:
            s.bub.push(choice(s.held_messages))
            s.last_held_message_time = now

    def _protective_think(s):
        """
        The fast-acting protective thread. Executes a combo if the target
        is too close or if the bot is being grabbed.
        """
        if not s.node.exists():
            return

        target = s._get_target()
        if isinstance(target,tuple):
            # powerup
            ty,target = target
        else:
            # player
            now = time()

            # Check if we are being held. If so, try to break free and say the urgent message.
            if target and target.hold_node == s.node and now - s.last_skill_time > 0.4:
                s._say_held()
                s.skill2()
                s.last_skill_time = now
                return

            # Only activate if a target exists and we are running (chasing)
            if target and s.node.run and now - s.last_skill_time > 0.4:
                my_pos = s.node.position
                target_pos = target.position
                distance = dist(my_pos, target_pos)

                # If the target is within a close range, use skill2 (punch + grab)
                if distance < 1.6:
                    s.skill2()
                    s.last_skill_time = now
        
    def _start_combos(s):
        """Starts the skill1 and shake combos on a regular timer."""
        s._say(choice(s.acquire_messages))
        s._skill1_timer = tock(0.4, s.skill1, repeat=True)
        s._shake_timer = tock(0.05, s._shake, repeat=True)
    
    def _stop_combos(s):
        """Stops the combos and resets the state."""
        if hasattr(s, '_skill1_timer') and s._skill1_timer: s._skill1_timer = None
        if hasattr(s, '_shake_timer') and s._shake_timer: s._shake_timer = None

    def skill1(s):
        """Executes a combo of button presses with delays, starting with jump and bomb."""
        s.on(0) # jump
        s.on(1) # bomb
        tick(0.04,lambda:s.on(2)) # pickup
        tick(0.07,lambda:s.on(3)) # punch

    def skill2(s):
        """Performs a punch-grab combo."""
        s.on(3) # punch
        tick(0.05, lambda: s.on(2)) # pickup after a delay

    def _get_target(s) -> 'Node | None':
        """Finds the closest 'spaz' node that is not itself and is not dead."""
        if not s.node.exists(): return None
        my_pos = s.node.position

        pup_nodes = []
        player_nodes = []
        for n in GN():
            try:
                if n.exists() and n.getnodetype() == 'spaz' and n.hurt < 1.0 and n is not s.node:
                    player_nodes.append(n)
                    continue
                ty = getattr(n.getdelegate(object),'poweruptype',0)
                if ty and dist(n.position,my_pos) > 5.5 or s.node.hold_node: continue
                match ty:
                    case 'health':
                        if s.node.hurt < 0.3: continue
                        pup_nodes.append((ty,n))
                    case 'punch':
                        if s.node.getdelegate(object)._has_boxing_gloves: continue
                        pup_nodes.append((ty,n))
                    case 'shield':
                        if (s.node.getdelegate(object).shield_hitpoints or 0) > 200: continue
                        pup_nodes.append((ty,n))
            except: pass
        s.greed = False
        if pup_nodes:
            s.greed = True
            return min(
                pup_nodes,
                key=lambda _: dist(my_pos, _[1].position)
            )
        if player_nodes:
            return min(
                player_nodes,
                key=lambda n: dist(my_pos, n.position)
            )

    def _shake(s):
        """Handles the rapid left/right shaking movement."""
        s.is_shaking = not s.is_shaking
        if s.is_shaking:
            s.move(0.5, 0.1) 
        else:
            s.move(-0.5, 0.1)

    def _avoid_void(s):
        activity = bs.get_foreground_host_activity()
        if not activity or not s.node.exists():
            return
        bounds = activity.map.get_play_bounds()
        min_x, max_x, min_y, max_y, min_z, max_z = bounds
        x, y, z = s.node.position
        margin = 0.8  # safety distance from edge
        # If too close to X edge
        if x < min_x + margin:
            s.move(1, 0)
        elif x > max_x - margin:
            s.move(-1, 0)
        # If too close to Z edge
        if z < min_z + margin:
            s.move(0, 1)
        elif z > max_z - margin:
            s.move(0, -1)

    def _think(s):
        """
        The main AI logic loop for the Ender bot.
        """
        if not s.node.exists():
            s._think_timer = None
            s._protective_timer = None
            s._stop_combos()
            return
        #s._avoid_void()
        now = time()
        target = s._get_target()
        if isinstance(target,tuple):
            ty,target = target
        else:
            # Player

            # Check for holding an incorrect or dead target
            if s.node.hold_node and (s.node.hold_node != target or (target and target.hurt == 1.0)):
                s._stop_combos()

                if s.node.hold_node and s.node.hold_node != target and target:
                    s._say(f"Why am I holding this")
                elif target and target.hurt == 1.0:
                    s._say(choice(s.release_messages))

                s.on(2) # Release pickup
                s.move(0, 0) # Stop moving for a moment
                s._has_announced_target = False # Reset the flag
                return

            # Shaking logic for when the *correct* player is held and they are still alive
            if s.node.hold_node == target:
                s.on_run(0) # Stop moving forward

                # Start combos if not already running
                if not s._skill1_timer:
                    s._start_combos()
                return

            # If we get here, we are not holding the target, so stop any combos
            s._stop_combos()

        if target and target.exists():
            # If we just found a new target, announce it.
            if not s._has_announced_target:
                if s.greed:
                    s.bub.push('')
                    s._say(choice(s.greed_messages))
                else:
                    # Instantly clear the 'lonely' message
                    s.bub.push('')
                    s._say(choice(s.pursuit_messages))
                s._has_announced_target = True

            my_pos = s.node.position
            target_pos = target.position
            distance = dist(my_pos, target_pos)

            # Calculate direction vector to the target (normalized)
            dx = target_pos[0] - my_pos[0]
            dz = target_pos[2] - my_pos[2]
            vector_length = (dx**2 + dz**2)**0.5

            if vector_length == 0:
                s.move(0, 0)
                return

            move_x = dx / vector_length
            move_z = dz / vector_length
            
            # Apply the run-reset logic to ensure responsive movement
            s.on_run(0)
            tick(0.02,lambda:s.on_run(1))
            
            # Occasionally say a pursuit message
            if random() < 0.05 and now - s.last_speech_time > s.speech_cooldown:
                s._say(choice(s.greed_messages if s.greed else s.pursuit_messages))

            # Move towards the target. The protective thread handles the close-range grab.
            s.move(move_x, -move_z)

        else:
            # No targets? Stop and chill.
            if s._has_announced_target:
                s._has_announced_target = False
                s.last_idle_chat_time = now + 2 # offset to talk faster
            # Cooldown is 5 seconds
            elif now - s.last_idle_chat_time > 5: 
                s._say(choice(s.idle_messages))
                s.last_idle_chat_time = now
            s.on_run(0) # Stop running
            s.move(0, 0)


GSW = lambda s: gsw(s,suppress_warning=True)
GSH = lambda s: gsh(s,suppress_warning=True)
TEX = lambda o,**k: newnode(
    'text',
    owner=o,
    attrs={
        'in_world':True,
        'scale':0.01,
        'flatness':1,
        'h_align':'center',
        **k
    }
)

# Keep track of all Ender bots we spawn
ender_instances = []
ENABLE_GLOVES = True
ENABLE_SHIELD = False

def check_player_count():
    """Spawn 1 Ender bot only when exactly 1 real player (excluding lobby) is in-game."""
    global ender_instances, BOTNAME
    activity = get_foreground_host_activity()
    if not activity:
        return

    try:
        session = bs.get_foreground_host_session()
        if not isinstance(session, (bs.FreeForAllSession, bs.DualTeamSession, bs.CoopSession)):
           return
        # Filter only "real" players (exclude ones not yet in-game / lobby placeholders)
        real_players = [
            sp for sp in session.sessionplayers
            if sp.getname() not in ("<in-lobby>", None, "")
        ]

        # Remove Enders that no longer exist
        ender_instances = [b for b in ender_instances if b.node.exists()]
        current_bots = len(ender_instances)

        if len(real_players) == 1:
            # One real player -> ensure exactly one Ender
            if current_bots < 1:
                ender_instances.append(Ender(name=BOTNAME))  # Use your custom name
            elif current_bots > 1:
                for _ in range(current_bots - 1):
                    bot = ender_instances.pop()
                    if bot.node.exists():
                        bot.node.delete()
    except Exception as e:
        print(f"[EnderBot] Error in check_player_count: {e}")


def check_player_count():
    """Spawn 1 Ender bot only when exactly 1 real player is in-game."""
    global ender_instances
    try:
        activity = get_foreground_host_activity()
        if not activity:
            return
        if not isinstance(activity, bs.GameActivity):
            return
        if not activity.has_begun() or activity.has_ended():
            return

        session = bs.get_foreground_host_session()
        if not isinstance(session, (bs.FreeForAllSession, bs.DualTeamSession)):
            return

        real_players = [
            sp for sp in session.sessionplayers
            if sp.getname() not in ('<in-lobby>', None, '')
        ]

        # Remove dead bots
        ender_instances = [b for b in ender_instances if b.node.exists()]
        current_bots = len(ender_instances)

        if len(real_players) <= 1:
            if current_bots < 1:
                print('[EnderBot] Spawning bot...')
                with activity.context:
                    ender_instances.append(Ender(name=BOTNAME))
        else:
            # Enough players — remove bots
            for bot in ender_instances:
                try:
                    if bot.node.exists():
                        bot.node.delete()
                except Exception:
                    pass
            ender_instances.clear()

    except Exception as e:
        print(f'[EnderBot] Error: {e}')


# ba_meta export babase.Plugin
class EnderPlugin(babase.Plugin):

    def on_app_running(self) -> None:
        global _ender_timer
        _ender_timer = babase.AppTimer(3.0, check_player_count, repeat=True)
        print('[EnderBot] Plugin active — checking every 3s.')
