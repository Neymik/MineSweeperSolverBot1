
mapa = '''0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0
? ? 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0
? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0
? ? 0 0 0 0 0 0 ? ? ? ? ? 0 0 ? ?
? ? 0 0 ? ? ? 0 ? ? ? ? ? 0 0 ? ?
? ? ? ? ? ? ? 0 ? ? ? 0 0 0 0 ? ?
? ? ? ? ? ? ? 0 ? ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ? ?
? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? ? ?
? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0 0
? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 0 0 ? ? ? ? ? 0
? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ?'''
result = '''0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0
1 1 0 0 0 1 3 3 3 1 1 0 0 0 0 0 0
x 3 2 2 1 3 x x 2 x 1 0 0 0 0 0 0
2 x x 2 x 3 x 3 2 1 1 0 0 0 0 0 0
1 2 2 2 1 2 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0
1 1 0 0 0 0 0 0 1 1 2 x 1 0 0 1 1
x 1 0 0 1 1 1 0 2 x 3 1 1 0 0 1 x
2 2 1 2 4 x 2 0 2 x 2 0 0 0 0 1 1
x 2 2 x x x 2 0 1 1 2 1 1 0 0 0 0
1 2 x 3 3 2 1 0 0 0 1 x 1 1 2 2 1
1 2 2 1 0 0 0 0 0 0 1 1 1 1 x x 1
1 x 2 2 1 1 0 0 0 0 0 0 1 2 3 2 1
1 2 x 2 x 2 1 1 0 0 0 0 1 x 1 0 0
1 2 1 2 1 2 x 1 0 0 0 1 2 3 2 1 0
x 1 0 0 0 1 1 1 0 0 0 2 x 4 x 2 0
1 1 0 0 0 0 0 0 0 0 1 3 x 4 x 2 0
0 0 0 0 0 0 0 0 0 0 1 x 2 2 2 3 2
1 1 0 0 0 1 1 1 0 0 1 1 2 1 3 x x
x 1 0 0 0 1 x 1 0 0 0 0 1 x 3 x 3'''
mines = 41

def open(row, column):
  point = mapMap(result)[row][column]
  if point == 'x':
    raise Exception('Game Over row ' + str(row) + ' column ' + str(column))
  return point

PRINT = True
MINE_SIMULATION_LIMIT = 20

def mapMap(mapa):
  return list(map(lambda row: row.split(' '), mapa.split('\n')))

def demapMap(mapa):
  return '\n'.join(map(lambda row: ' '.join(list(map(lambda col: str(col),row))), mapa))

def copyMap(mapa):
  return [x[:] for x in mapa] # optimization

def solve_mine(map, minesTotal):

  mapArray = mapMap(map)
  actions = []
  minesSet = 0

  def runThroughMap(runner):
    for row in range (0, len(mapArray)):
      for col in range (0, len(mapArray[0])):
        runner(row, col)

  def doAround(func, row, col): # optimization

    returnArray = []

    mapArrayRowLen = len(mapArray)
    mapArrayColLen = len(mapArray[0])
    colm1 = col - 1 >= 0
    colp1 = col + 1 < mapArrayColLen

    if (row + 1 < mapArrayRowLen):
      returnArray.append(func(row + 1, col    ))
      if (colp1):
        returnArray.append(func(row + 1, col + 1))
      if (colm1):
        returnArray.append(func(row + 1, col - 1))

    if (row - 1 >= 0):
      returnArray.append(func(row - 1, col    ))
      if (colp1):
        returnArray.append(func(row - 1, col + 1))
      if (colm1):
        returnArray.append(func(row - 1, col - 1))
    
    if (colp1):
      returnArray.append(func(row    , col + 1))
    if (colm1):
      returnArray.append(func(row    , col - 1))

    return returnArray

  def openAround(row, col):
    doAround(openPoint, row, col)
  def openPoint(row, col):
    if (mapArray[row][col] == '?'):
      mapArray[row][col] = open(row, col)
      actions.append({
        'action': checkPoint,
        'row': row,
        'col': col
      })

  def getAround(row, col):
    return doAround(getPoint, row, col)
  def getPoint(row, col):
    return mapArray[row][col]

  def checkPoint(row, col):
    point = getPoint(row, col)
    if (point == 'x' or point == '?'):
      return

    pointsAround = getAround(row, col)
    minesAround = len(list(filter(lambda point: point == 'x', pointsAround)))
    questionsAround = len(list(filter(lambda point: point == '?', pointsAround)))
    if (not questionsAround):
      return
    if ((int(point) - minesAround) == questionsAround):
      actions.append({
        'action': setMineAround,
        'row': row,
        'col': col
      })
    elif (int(point) == minesAround):
      actions.append({
        'action': openAround,
        'row': row,
        'col': col
      })

  def setMineAround(row, col):
    doAround(setMinePoint, row, col)
  def setMinePoint(row, col):
    nonlocal minesSet
    if (mapArray[row][col] == '?'):
      mapArray[row][col] = 'x'
      minesSet += 1

  def tryFindIntersections():

    pointsNearQuestions = []

    def pointsNearQuestionsChecker(row, col):
      if (mapArray[row][col] != '?' and mapArray[row][col] != 'x'):

        pointsAround = doAround(
          lambda row1, col1: {
            'row': row1,
            'col': col1
          }, row, col)
        questionsAround = list(filter(lambda point: mapArray[point['row']][point['col']] == '?', pointsAround))

        if (len(questionsAround)):
          minesAround = list(filter(lambda point: mapArray[point['row']][point['col']] == 'x', pointsAround))
          pointsNearQuestions.append({
            'questionsAround': questionsAround,
            'minesAround': minesAround,
            'row': row,
            'col': col
          })

    def getPointPairs():
      pointPairs = []
      for i in range (0, len(pointsNearQuestions)):
        pointFirst = pointsNearQuestions[i]
        for j in range (0, len(pointsNearQuestions)):
          pointSecond = pointsNearQuestions[j]
          if (i == j):
            continue
          pointPairIntersections = getPointPairIntersections(pointFirst, pointSecond)
          if (not pointPairIntersections):
            continue
          pointPairs.append({
            'pointPairIntersections': pointPairIntersections,
            'pointFirst': pointFirst,
            'pointSecond': pointSecond
          })
      return pointPairs

    def getPointPairIntersections(pointFirst, pointSecond):
      pointsAroundFirst = pointFirst['questionsAround']
      pointsAroundSecond = pointSecond['questionsAround']
      pointsIntersections = []

      for i in range (0, len(pointsAroundFirst)):
        pointAroundFirst = pointsAroundFirst[i]
        for j in range (0, len(pointsAroundSecond)):
          pointAroundSecond = pointsAroundSecond[j]
          if (pointAroundFirst['row'] == pointAroundSecond['row'] and pointAroundFirst['col'] == pointAroundSecond['col']):
            pointsIntersections.append(pointAroundFirst)

      if (not len(pointsIntersections)):
        return False
      return pointsIntersections

    runThroughMap(lambda row, col:
      pointsNearQuestionsChecker(row, col)
    )

    pointPairs = getPointPairs()

    for i in range (0, len(pointPairs)):
      pointPair = pointPairs[i]
      pointFirst = pointPair['pointFirst']
      pointSecond = pointPair['pointSecond']

      pointPairIntersectionsCount = len(pointPair['pointPairIntersections'])

      pointFirstQuestionsAroundCount = len(pointFirst['questionsAround'])
      pointFirstMinesTotalAroundCount = int(mapArray[pointFirst['row']][pointFirst['col']])
      pointFirstMinesSetAroundCount = len(pointFirst['minesAround'])
      pointFirstMinesOutsideIntersectionPessimistic = pointFirstQuestionsAroundCount - pointPairIntersectionsCount + pointFirstMinesSetAroundCount
      pointFirstMinesAtIntersectionMinimal = pointFirstMinesTotalAroundCount - pointFirstMinesOutsideIntersectionPessimistic

      pointSecondQuestionsAroundCount = len(pointSecond['questionsAround'])
      pointSecondMinesTotalAroundCount = int(mapArray[pointSecond['row']][pointSecond['col']])
      pointSecondMinesSetAroundCount = len(pointSecond['minesAround'])
      pointSecondMinesUndetectedAround = pointSecondMinesTotalAroundCount - pointSecondMinesSetAroundCount

      if (pointPairIntersectionsCount >= pointSecondQuestionsAroundCount): # optimization
        continue

      if (pointFirstMinesAtIntersectionMinimal == pointSecondMinesUndetectedAround):
        for j in range (0, len(pointSecond['questionsAround'])):
          currentQuestion = pointSecond['questionsAround'][j]
          isIntersection = False

          for k in range (0, len(pointPair['pointPairIntersections'])):
            currentIntersection = pointPair['pointPairIntersections'][k]
            if (currentQuestion['row'] == currentIntersection['row'] and currentQuestion['col'] == currentIntersection['col']):
              isIntersection = True
              break

          if (isIntersection):
            continue

          openPoint(currentQuestion['row'], currentQuestion['col'])

        return True

    return False


  def trySimulateMines():
    nonlocal minesSet

    remainingMines = minesTotal - minesSet
    questionPoints = []
    mapCopy = []
    validArragements = []
    questionPointsAway = []

    def checkValidArragements():
      for row in range (0, len(mapArray)):
        for col in range (0, len(mapArray[0])):
          if (mapCopy[row][col] == 'x' or mapCopy[row][col] == '?'):
            continue
          pointsAround = doAround(
            lambda row1, col1: 
              mapCopy[row1][col1]
            , row, col)
          minesAround = len(list(filter(lambda point1: point1 == 'x', pointsAround)))
          
          if (int(mapCopy[row][col]) != minesAround):
            return False
      return True

    def getCombinations(array, count):
      combinations = []
      
      if (count == 1):
        for i in range (0, len(array)):
          combinations.append([array[i]])
        return combinations

      for i in range (0, len(array)):

        combinations1 = getCombinations(array[i + 1:], count - 1)
        for j in range (0, len(combinations1)):
          combinations1[j].insert(0, array[i])
        combinations.extend(combinations1)

      return combinations

    def setupQuestionPoints(row, col):
      if (mapArray[row][col] == '?'):
        pointsAround = doAround(
          lambda row1, col1: 
            mapArray[row1][col1]
          , row, col)
        notQuestionsAround = len(list(filter(lambda point1: point1 != '?', pointsAround)))
        if (notQuestionsAround):
          questionPoints.append({
            'row': row,
            'col': col
          })
        else:
          questionPointsAway.append({
            'row': row,
            'col': col
          })

    # optimization
    runThroughMap(setupQuestionPoints)
    awayMinesPlacesCount = min(remainingMines, len(questionPointsAway))
    questionPoints.extend(questionPointsAway[:awayMinesPlacesCount + 1])

    if (remainingMines > MINE_SIMULATION_LIMIT):
      print('Too many mines to simulate!')
      return False

    combinations = getCombinations(questionPoints, remainingMines)

    for i in range (0, len(combinations)):
      mapCopy = copyMap(mapArray)

      for j in range (0, len(combinations[i])):
        point = combinations[i][j]
        mapCopy[point['row']][point['col']] = 'x'

      validArragement = checkValidArragements()

      if (not validArragement):
        continue

      validArragements.append(mapCopy)

      # if (PRINT):
      #   print('combination', combinations[i])
      #   print('mapCopy', mapCopy)

    # if (PRINT):
    #   print('validArragements', len(validArragements[0]))
    #   print('firstValidArragement', demapMap(validArragements[0]))

    if (not len(validArragements)):
      return False

    if (len(validArragements) == 1):
      minesSet = minesTotal
      return validArragements[0]

    # check if there is a mine or no mine at the same place in all valid arragements
    mapWithSameMines = copyMap(mapArray)
    thereIsTheSame = False

    def sameMinesSetRunner (row, col):
      if (validArragements[i][row][col] == 'x'):
        if (mapWithSameMines[row][col] == '?'):
          mapWithSameMines[row][col] = {
            'sameMines': 1
          }
        elif (type(mapWithSameMines[row][col]) is dict):
          mapWithSameMines[row][col]['sameMines'] += 1

    for i in range (0, len(validArragements)):
      runThroughMap(sameMinesSetRunner)
    
    for i in range (0, len(questionPoints)):
      point = questionPoints[i]
      if (mapWithSameMines[point['row']][point['col']] == '?'):
        thereIsTheSame = True
        openPoint(point['row'], point['col'])
      elif (type(mapWithSameMines[point['row']][point['col']]) is dict):
        if (mapWithSameMines[point['row']][point['col']]['sameMines'] == len(validArragements)):
          thereIsTheSame = True
          mapArray[point['row']][point['col']] = 'x'
          minesSet += 1

    if (PRINT):
      print(demapMap(mapWithSameMines))

    return thereIsTheSame


  while (True):
    if (PRINT): 
      print('cycle================cycle')
    cycleStartMap = demapMap(mapArray)
    runThroughMap(lambda row, col:
      actions.append({
        'action': checkPoint,
        'row': row,
        'col': col
      })
    )

    while (len(actions)):
      if (PRINT):
        print(demapMap(mapArray))
      action = actions.pop(0)
      if (PRINT):
        print(action)
      action['action'](action['row'], action['col'])

    cycleEndMap = demapMap(mapArray)

    if (cycleStartMap == cycleEndMap):
      if (minesSet != minesTotal):
        tryFindIntersectionsResult = tryFindIntersections()
        if (tryFindIntersectionsResult):
          continue
        trySimulateMinesResult = trySimulateMines()
        if (trySimulateMinesResult):
          if (type(trySimulateMinesResult) is list):
            mapArray = trySimulateMinesResult
          continue
      if (PRINT):
        print(demapMap(mapArray))
      break

    cycleEndMap = demapMap(mapArray)

  if (PRINT):
    print('minesSet', minesSet, 'minesTotal', minesTotal)

  if (minesSet != minesTotal):
    return '?'

  # check if all questions are opened
  runThroughMap(lambda row, col:
    openPoint(row, col) if mapArray[row][col] == '?' else None
  )

  return demapMap(mapArray)



print(solve_mine(mapa, mines))

# import cProfile
# for i in range(10):
#   cProfile.run('solve_mine(mapa, mines)', 'perfstats')
# import pstats
# from pstats import SortKey
# p = pstats.Stats('perfstats')
# p.sort_stats(SortKey.CUMULATIVE).print_stats()
