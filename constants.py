body_base_commands = ['command_move',
                      'command_rotate_left', 'command_rotate_right',
                      'command_regenerate',
                      'command_split',
                      'command_give']
body_attack_commands = ['command_eat',
                        'command_attack',
                        'command_freeze',
                        'command_wall_1', 'command_wall_2']
body_memory_commands = ['command_memory_1_set', 'command_memory_1_value', 'command_memory_1_erase',
                        'command_memory_2_set', 'command_memory_2_value', 'command_memory_2_erase']
body_speak_commands = ['command_voice_speak', 'command_voice_whisper', 'command_voice_1_value', 'command_voice_2_value',
                       'command_voice_3_value']

body_state_commands = ['command_set_state', 'command_erase_state', 'command_state_value']
body_reflect_commands = ['command_reflect_1', 'command_reflect_2', 'command_reflect_3']
body_sentient_commands = ['command_memorize', 'command_think'] + body_state_commands + body_reflect_commands
body_dna_commands = ['command_dna_save', 'command_dna_choose', 'command_dna_erase']

body_commands = body_base_commands + body_attack_commands \
                + body_memory_commands + body_speak_commands \
                + body_sentient_commands + body_dna_commands
sight = ['see_red', 'see_green', 'see_blue', 'see_health', 'see_happyness',
         'see_state', 'see_frozen', 'see_attacking',
         'see_distance_0', 'see_distance_1', 'see_distance_2', 'see_distance_3',
         'see_looking', 'see_orientation']
ddddd = ['north', 'south',
         'west', 'westwest', 'east', 'easteast',
         'northwest', 'northwestwest',
         'northeast', 'northeasteast',
         'southwest', 'southeast',
         'northnorth', 'northnorthnorth', 'northnorthnorthnorth',
         'northnorthwest', 'northnorthwestwest', 'northnorthwestwestwest',
         'northnortheast', 'northnortheasteast',
         'northnortheasteasteast',
         'northnorthnorthwest', 'northnorthnortheast']
surounding_sense = []
for i in ddddd:
    surounding_sense.append('sense_' + str(i))
print(surounding_sense)
sense = [
    'sense_memory_1', 'sense_memory_2', 'sense_health',
    'sense_sound_1', 'sense_sound_2', 'sense_sound_3',
    'sense_happy', 'sense_killed', 'sense_state',
    'sense_alive_0', 'sense_alive_1', 'sense_alive_2',
    'sense_frozen',
    'sense_pos_x', 'sense_pos_y',
    'sense_clock', 'sense_reflect_1', 'sense_reflect_2', 'sense_reflect_3']

body_perception = sight + sense + surounding_sense

brain_all_neuron_names = body_commands + body_perception
for i in range(int(len(list(brain_all_neuron_names)) / 2)):
    brain_all_neuron_names.append('Hidden_' + str(i))

print('brain size: ', len(brain_all_neuron_names))

pygame_windows_size = [1920, 1020]

constant_grid_size = 100
constant_suns = int(2 / 10000 * constant_grid_size ** 2 + 0.5)

brain_min_dna_length = 1
brain_max_dna_length = int(len(brain_all_neuron_names))
neuron_weight_size = 100
neuron_weight_scale = 10
brain_drain_scale = 0

handler_random_mutationrate = 1
handler_mutationrate = 95
handler_amount_larticles = int(constant_grid_size ** (2) / 10)
handler_click_error = 0.8
handler_random_larticles_amount = 300
handler_death_at_birth = 20  # %

neuron_learningrate = 0.5
neurons_connectiondepth = 5

body_health_bar = 500
body_max_health = 3 * body_health_bar
body_suffer = 0.2
body_splitrate_red = 2
body_splitrate_attacker = 1
body_eat_damage = body_health_bar / 2
body_attack_damage = body_eat_damage
body_freeztime = 3
body_freeze_delay = 5
body_wall_drain = body_health_bar / 50
body_eat_health_gain = 0.8
body_regenrate = 10
body_clock_interval = 10

body_colour_newborn = [1, 1, 1]
body_colour_inactive = [0, 1, 0]
body_colour_regenerating = [0, 0, 1]
body_colour_eating = [1, 0, 0]
body_colour_attacking_eating = [1, 0.5, 0]
body_colour_attacking_regenerating = [0, 0.5, 1]
body_colour_attacking_else = [1, 1, 0]
body_colour_wall = [0.5, 0.5, 0.5]

testing = True

body_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
