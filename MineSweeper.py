

MAPA = '''0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ?
? ? 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 ? ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0'''
RESULT = '''0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0'''
MINES = 16

def open(row, column): # assumed to be a task description
  point = map_matrix[row][column]
  if point == 'x':
    raise Exception(f'Game Over row {row} column {column} is a mine')
  return point

PRINT = False
MINE_SIMULATION_LIMIT = 20

def matrix_to_list(mapa):
  return list(map(lambda row: row.split(' '), mapa.split('\n')))

map_matrix = matrix_to_list(RESULT)

def matrix_to_string(mapa):
  return '\n'.join(map(lambda row: ' '.join(map(str, row)), mapa))

def copy_matrix(mapa):
  return [x[:] for x in mapa] # optimization

def solve_mine(gameMap, mines_total):

  map_array = matrix_to_list(gameMap)
  actions = []
  mines_set = 0

  def run_through_map(runner):
    for row in range(0, len(map_array)):
      for col in range(0, len(map_array[0])):
        runner(row, col)

  def do_around(func, row, col): # optimization

    result = []

    map_array_row_len = len(map_array)
    map_array_col_len = len(map_array[0])
    has_prev_col = col - 1 >= 0
    has_next_col = col + 1 < map_array_col_len

    if row + 1 < map_array_row_len:
      result.append(func(row + 1, col    ))
      if has_next_col:
        result.append(func(row + 1, col + 1))
      if has_prev_col:
        result.append(func(row + 1, col - 1))

    if row - 1 >= 0:
      result.append(func(row - 1, col    ))
      if has_next_col:
        result.append(func(row - 1, col + 1))
      if has_prev_col:
        result.append(func(row - 1, col - 1))
    
    if has_next_col:
      result.append(func(row    , col + 1))
    if has_prev_col:
      result.append(func(row    , col - 1))

    return result

  def open_around(row, col):
    do_around(open_point, row, col)
  def open_point(row, col):
    if map_array[row][col] == '?':
      map_array[row][col] = open(row, col)
      actions.append({
        'action': check_point,
        'row': row,
        'col': col
      })

  def get_around(row, col):
    return do_around(get_point, row, col)
  def get_point(row, col):
    return map_array[row][col]

  def check_point(row, col):
    point = get_point(row, col)
    if point == 'x' or point == '?':
      return

    points_around = get_around(row, col)
    mines_around = len(list(filter(lambda point: point == 'x', points_around)))
    questions_around = len(list(filter(lambda point: point == '?', points_around)))
    if not questions_around:
      return
    if (int(point) - mines_around) == questions_around:
      actions.append({
        'action': set_mine_around,
        'row': row,
        'col': col
      })
    elif int(point) == mines_around:
      actions.append({
        'action': open_around,
        'row': row,
        'col': col
      })

  def set_mine_around(row, col):
    do_around(set_mine_point, row, col)
  def set_mine_point(row, col):
    nonlocal mines_set
    if map_array[row][col] == '?':
      map_array[row][col] = 'x'
      mines_set += 1

  def try_find_intersections():

    points_near_questions = []

    def points_near_questions_checker(row, col):
      if map_array[row][col] in '?x':
        return

      points_around = do_around(
        lambda row1, col1: {
          'row': row1,
          'col': col1
        }, row, col)
      questions_around = list(filter(lambda point: map_array[point['row']][point['col']] == '?', points_around))

      if questions_around:
        mines_around = list(filter(lambda point: map_array[point['row']][point['col']] == 'x', points_around))
        points_near_questions.append({
          'questions_around': questions_around,
          'mines_around': mines_around,
          'row': row,
          'col': col
        })

    def get_point_pairs():
      point_pairs = []
      for i in range (0, len(points_near_questions)):
        point_first = points_near_questions[i]
        for j in range (0, len(points_near_questions)):
          point_second = points_near_questions[j]
          if i == j:
            continue
          point_pair_intersections = get_point_pair_intersections(point_first, point_second)
          if not point_pair_intersections:
            continue
          point_pairs.append({
            'point_pair_intersections': point_pair_intersections,
            'point_first': point_first,
            'point_second': point_second
          })
      return point_pairs

    def get_point_pair_intersections(point_first, point_second):
      points_around_first = point_first['questions_around']
      points_around_second = point_second['questions_around']
      points_intersections = []

      for point_around_first in points_around_first:
        for point_around_second in points_around_second:
          if point_around_first['row'] == point_around_second['row'] and point_around_first['col'] == point_around_second['col']:
            points_intersections.append(point_around_first)

      if not points_intersections:
        return False
      return points_intersections

    run_through_map(lambda row, col:
      points_near_questions_checker(row, col)
    )

    point_pairs = get_point_pairs()

    for point_pair in point_pairs:
      p1 = point_pair['point_first']
      p2 = point_pair['point_second']

      point_pair_intersections = len(point_pair['point_pair_intersections'])

      p1_questions_around = len(p1['questions_around'])
      p1_mines_total_around = int(map_array[p1['row']][p1['col']])
      p1_mines_set_around = len(p1['mines_around'])
      p1_mines_outside_intersection_pessimistic = p1_questions_around - point_pair_intersections + p1_mines_set_around
      p1_mines_at_intersection_minimal = p1_mines_total_around - p1_mines_outside_intersection_pessimistic

      p2_questions_around = len(p2['questions_around'])
      p2_mines_total_around_count = int(map_array[p2['row']][p2['col']])
      p2_mines_set_around_count = len(p2['mines_around'])
      p2_mines_undetected_around = p2_mines_total_around_count - p2_mines_set_around_count

      if point_pair_intersections >= p2_questions_around: # optimization
        continue

      if p1_mines_at_intersection_minimal == p2_mines_undetected_around:
        for current_question in p2['questions_around']:
          is_intersection = False

          for current_intersection in point_pair['point_pair_intersections']:
            if current_question['row'] == current_intersection['row'] and current_question['col'] == current_intersection['col']:
              is_intersection = True
              break

          if is_intersection:
            continue

          open_point(current_question['row'], current_question['col'])

        return True

    return False


  def try_simulate_mines():
    nonlocal mines_set

    remaining_mines = mines_total - mines_set

    if remaining_mines > MINE_SIMULATION_LIMIT:
      print('Too many mines to simulate!')
      return False

    question_points = []
    map_copy = []
    valid_arragements = []
    question_points_away = []

    def check_valid_arragements():
      for row in range (0, len(map_array)):
        for col in range (0, len(map_array[0])):
          if map_copy[row][col] in 'x?':
            continue
          points_around = do_around(
            lambda row1, col1:
              map_copy[row1][col1]
            , row, col)
          mines_around = len(list(filter(lambda point1: point1 == 'x', points_around)))
          
          if int(map_copy[row][col]) != mines_around:
            return False
      return True

    def get_combinations(array, count):
      combinations = []
      
      if count == 1:
        for i in range (0, len(array)):
          combinations.append([array[i]])
        return combinations

      for i in range (0, len(array)):

        combinations1 = get_combinations(array[i + 1:], count - 1)
        for j in range (0, len(combinations1)):
          combinations1[j].insert(0, array[i])
        combinations.extend(combinations1)

      return combinations

    def setup_question_points(row, col):
      if map_array[row][col] == '?':
        return
      points_around = do_around(
        lambda row1, col1:
          map_array[row1][col1]
        , row, col)
      not_questions_around = len(list(filter(lambda point1: point1 != '?', points_around)))
      if not_questions_around:
        question_points.append({
          'row': row,
          'col': col
        })
      else:
        question_points_away.append({
          'row': row,
          'col': col
        })

    # optimization
    run_through_map(setup_question_points)
    away_mines_places_count = min(remaining_mines, len(question_points_away))
    question_points.extend(question_points_away[:away_mines_places_count + 1])

    combinations = get_combinations(question_points, remaining_mines)

    for combination in combinations:
      map_copy = copy_matrix(map_array)

      for point in combination:
        map_copy[point['row']][point['col']] = 'x'

      valid_arragement = check_valid_arragements()

      if not valid_arragement:
        continue

      valid_arragements.append(map_copy)

      # if PRINT:
      #   print('combination', combinations[i])
      #   print('map_copy', map_copy)

    # if PRINT:
    #   print('valid_arragements', len(valid_arragements[0]))
    #   print('firstvalid_arragement', matrix_to_string(valid_arragements[0]))

    if not valid_arragements:
      return False

    if len(valid_arragements) == 1:
      mines_set = mines_total
      return valid_arragements[0]

    # check if there is a mine or no mine at the same place in all valid arragements
    map_with_same_mines = copy_matrix(map_array)
    there_is_the_same = False

    def same_mines_set_runner (row, col):
      if valid_arragement[row][col] == 'x':
        if map_with_same_mines[row][col] == '?':
          map_with_same_mines[row][col] = {
            'same_mines': 1
          }
        elif type(map_with_same_mines[row][col]) is dict:
          map_with_same_mines[row][col]['same_mines'] += 1

    for valid_arragement in valid_arragements:
      run_through_map(same_mines_set_runner)
    
    for point in question_points:
      if map_with_same_mines[point['row']][point['col']] == '?':
        there_is_the_same = True
        open_point(point['row'], point['col'])
      elif type(map_with_same_mines[point['row']][point['col']]) is dict:
        if map_with_same_mines[point['row']][point['col']]['same_mines'] == len(valid_arragements):
          there_is_the_same = True
          map_array[point['row']][point['col']] = 'x'
          mines_set += 1

    if PRINT:
      print(matrix_to_string(map_with_same_mines))

    return there_is_the_same


  while True:
    if PRINT: 
      print('cycle================cycle')
    cycle_start_map = matrix_to_string(map_array)
    run_through_map(lambda row, col:
      actions.append({
        'action': check_point,
        'row': row,
        'col': col
      })
    )

    while actions:
      if PRINT:
        print(matrix_to_string(map_array))
      action = actions.pop(0)
      if PRINT:
        print(action)
      action['action'](action['row'], action['col'])

    cycle_end_map = matrix_to_string(map_array)

    if cycle_start_map == cycle_end_map:
      if mines_set != mines_total:
        try_find_intersections_result = try_find_intersections()
        if try_find_intersections_result:
          continue
        try_simulate_mines_result = try_simulate_mines()
        if try_simulate_mines_result:
          if type(try_simulate_mines_result) is list:
            map_array = try_simulate_mines_result
          continue
      if PRINT:
        print(matrix_to_string(map_array))
      break

    cycle_end_map = matrix_to_string(map_array)

  if PRINT:
    print('mines_set', mines_set, 'mines_total', mines_total)

  if mines_set != mines_total:
    return '?'

  # check if all questions are opened
  run_through_map(lambda row, col:
    open_point(row, col) if map_array[row][col] == '?' else None
  )

  return matrix_to_string(map_array)


import datetime 
a = datetime.datetime.now()
print(a)
solve_mine(MAPA, MINES)
b = datetime.datetime.now()
print(b)
print(b - a)

# import cProfile
# for i in range(1):
#   cProfile.run('solve_mine(MAPA, MINES)', 'perfstats')
# import pstats
# from pstats import SortKey
# p = pstats.Stats('perfstats')
# p.sort_stats(SortKey.CUMULATIVE).print_stats()
