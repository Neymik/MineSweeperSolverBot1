
const map = 
`0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0
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
? ? 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ?`;
const result =
`0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0
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
x 1 0 0 0 1 x 1 0 0 0 0 1 x 3 x 3`;
const mines = 41;

function open(row, column) {
  const point = mapMap(result)[row][column];
  if (point === 'x') {
    throw new Error('Game Over row ' + row + ' column ' + column);
  }
  return point;
}

const LOG = true;
const MINE_SIMULATION_LIMIT = 20;

function mapMap(map) {
  return map.split('\n').map(row => row.split(' '));
}

function demapMap(map) {
  return map.map(row => row.join(' ')).join('\n');
}

function solveMine(map, minesTotal) {
  
  let mapArray = mapMap(map);
  const actions = [];
  let minesSet = 0;

  while (true) {
    if (LOG) console.log('cycle================cycle');
    const cycleStartMap = demapMap(mapArray);
    runThroughMap((row, col) => {
      actions.push({
        action: checkPoint,
        row,
        col
      });
    });

    while (actions.length) {
      if (LOG) console.log(demapMap(mapArray));
      const action = actions.shift();
      if (LOG) console.log(action);
      action.action(action.row, action.col);
    }

    let cycleEndMap = demapMap(mapArray);

    if (cycleStartMap === cycleEndMap) {
      if (minesSet !== minesTotal) {
        const tryFindIntersectionsResult = tryFindIntersections();
        if (tryFindIntersectionsResult) {
          continue;
        }
        const trySimulateMinesResult = trySimulateMines();
        if (trySimulateMinesResult) {
          if (trySimulateMinesResult.length) {
            mapArray = trySimulateMinesResult;
          }
          continue;
        }
      }
      if (LOG) console.log(demapMap(mapArray));
      break;
    }

    cycleEndMap = demapMap(mapArray);
  }

  if (LOG) console.log('minesSet', minesSet, 'minesTotal', minesTotal);

  if (minesSet !== minesTotal) {
    return '?';
  }

  // check if all questions are opened
  runThroughMap((row, col) => {
    if (mapArray[row][col] === '?') {
      openPoint(row, col);
    }
  });

  return demapMap(mapArray);

  function runThroughMap(runner) {
    for (let row = 0; row < mapArray.length; row++) {
      for (let col = 0; col < mapArray[0].length; col++) {
        runner(row, col);
      }
    }
  }

  function doAround(func, row, col) {

    const returnArray = [];

    // doPoint(row    , col    )
    doPoint(row + 1, col    )
    doPoint(row + 1, col + 1)
    doPoint(row + 1, col - 1)
    doPoint(row - 1, col    )
    doPoint(row - 1, col + 1)
    doPoint(row - 1, col - 1)
    doPoint(row    , col + 1)
    doPoint(row    , col - 1)

    return returnArray

    function doPoint(row1, col1) {
      if (mapArray[row1] !== undefined && mapArray[row1][col1] !== undefined) {
        returnArray.push(func(row1, col1))
      }
    }

  }

  function openAround(row, col) {
    doAround(openPoint, row, col)
  }
  function openPoint(row, col) {
    if (mapArray[row][col] == '?') {
      mapArray[row][col] = open(row, col)
      actions.push({
        action: checkPoint,
        row,
        col
      });
    }
  }

  function getAround(row, col) {
    return doAround(getPoint, row, col);
  }
  function getPoint(row, col) {
    return mapArray[row][col];
  }

  function checkAround(row, col) {
    return doAround(checkPoint, row, col);
  }
  function checkPoint(row, col) {
    const point = getPoint(row, col);
    if (point === 'x' || point === '?') {
      return;
    }
    const pointsAround = getAround(row, col);
    const minesAround = pointsAround.filter(point => point === 'x').length;
    const questionsAround = pointsAround.filter(point => point === '?').length;
    if (!questionsAround) {
      return;
    }
    if ((point - minesAround) == questionsAround) {
      actions.push({
        action: setMineAround,
        row,
        col
      });
    } else if (point == minesAround) {
      actions.push({
        action: openAround,
        row,
        col
      });
    }
  }

  function setMineAround(row, col) {
    doAround(setMinePoint, row, col);
  }
  function setMinePoint(row, col) {
    if (mapArray[row][col] == '?') {
      mapArray[row][col] = 'x';
      minesSet++;
    }
  }


  function tryFindIntersections() {

    const pointsNearQuestions = [];

    runThroughMap((row, col) => {
      if (mapArray[row][col] !== '?' && mapArray[row][col] !== 'x') {

        const pointsAround = doAround((row1, col1) => {
          return {
            row: row1,
            col: col1
          }
        }, row, col);
        const questionsAround = pointsAround.filter(point => mapArray[point.row][point.col] === '?');

        if (questionsAround.length) {
          const minesAround = pointsAround.filter(point => mapArray[point.row][point.col] === 'x');
          pointsNearQuestions.push({
            questionsAround,
            minesAround,
            row,
            col
          });
        }
      }
    });

    const pointPairs = getPointPairs();

    for (let i = 0; i < pointPairs.length; i++) {
      const pointPair = pointPairs[i];
      const pointFirst = pointPair.pointFirst;
      const pointSecond = pointPair.pointSecond;

      const pointPairIntersectionsCount = pointPair.pointPairIntersections.length;

      const pointFirstQuestionsAroundCount = pointFirst.questionsAround.length;
      const pointFirstMinesTotalAroundCount = Number(mapArray[pointFirst.row][pointFirst.col]);
      const pointFirstMinesSetAroundCount = pointFirst.minesAround.length;
      const pointFirstMinesOutsideIntersectionPessimistic = pointFirstQuestionsAroundCount - pointPairIntersectionsCount + pointFirstMinesSetAroundCount;
      const pointFirstMinesAtIntersectionMinimal = pointFirstMinesTotalAroundCount - pointFirstMinesOutsideIntersectionPessimistic;

      const pointSecondQuestionsAroundCount = pointSecond.questionsAround.length;
      const pointSecondMinesTotalAroundCount = Number(mapArray[pointSecond.row][pointSecond.col]);
      const pointSecondMinesSetAroundCount = pointSecond.minesAround.length;
      const pointSecondMinesUndetectedAround = pointSecondMinesTotalAroundCount - pointSecondMinesSetAroundCount;

      if (pointPairIntersectionsCount >= pointSecondQuestionsAroundCount) { // optimization
        continue;
      }

      if (pointFirstMinesAtIntersectionMinimal == pointSecondMinesUndetectedAround) {
        for (let j = 0; j < pointSecond.questionsAround.length; j++) {
          const currentQuestion = pointSecond.questionsAround[j];
          let isIntersection = false;

          for (let k = 0; k < pointPair.pointPairIntersections.length; k++) {
            const currentIntersection = pointPair.pointPairIntersections[k];
            if (currentQuestion.row === currentIntersection.row && currentQuestion.col === currentIntersection.col) {
              isIntersection = true;
              break;
            } 
          }

          if (isIntersection) {
            continue;
          }

          openPoint(currentQuestion.row, currentQuestion.col);

        }
        return true;

      }
    }

    return false;

    function getPointPairs() {
      const pointPairs = [];
      for (let i = 0; i < pointsNearQuestions.length; i++) {
        const pointFirst = pointsNearQuestions[i];
        for (let j = 0; j < pointsNearQuestions.length; j++) {
          const pointSecond = pointsNearQuestions[j];
          if (i === j) {
            continue;
          }
          const pointPairIntersections = getPointPairIntersections(pointFirst, pointSecond);
          if (!pointPairIntersections) {
            continue;
          }
          pointPairs.push({
            pointPairIntersections,
            pointFirst,
            pointSecond
          });
        }
      }
      return pointPairs;
    }

    function getPointPairIntersections(pointFirst, pointSecond) {
      const pointsAroundFirst = pointFirst.questionsAround;
      const pointsAroundSecond = pointSecond.questionsAround;
      const pointsIntersections = [];

      for (let i = 0; i < pointsAroundFirst.length; i++) {
        const pointAroundFirst = pointsAroundFirst[i];
        for (let j = 0; j < pointsAroundSecond.length; j++) {
          const pointAroundSecond = pointsAroundSecond[j];
          if (pointAroundFirst.row === pointAroundSecond.row && pointAroundFirst.col === pointAroundSecond.col) {
            pointsIntersections.push(pointAroundFirst);
          }
        }
      }

      if (!pointsIntersections.length) {
        return false;
      }
      return pointsIntersections;
    }

  }


  function trySimulateMines() {

    const remainingMines = minesTotal - minesSet;
    const questionPoints = [];

    runThroughMap((row, col) => {
      if (mapArray[row][col] === '?') {
        questionPoints.push({
          row,
          col
        });
      }
    });

    if (remainingMines > MINE_SIMULATION_LIMIT) {
      console.log('Too many mines to simulate!');
      return false;
    }

    const combinations = getCombinations(questionPoints, remainingMines);
    let mapCopy = [];
    let lastValidMap = [];
    let validArragements = [];

    for (let i = 0; i < combinations.length; i++) {
      mapCopy = mapMap(demapMap(mapArray))

      for (let j = 0; j < combinations[i].length; j++) {
        const point = combinations[i][j];
        mapCopy[point.row][point.col] = 'x';
      }

      const validArragement = checkValidArragements();

      if (!validArragement) {
        continue;
      }

      validArragements.push(mapMap(demapMap(mapCopy)));

      // console.log('combination', combinations[i])
      // console.log('mapCopy', mapCopy)

    }

    // console.log('validArragements', validArragements)

    if (!validArragements.length) {
      return false;
    }

    if (validArragements.length === 1) {
      minesSet = minesTotal;
      return validArragements[0];
    }

    // check if there is a mine or no mine at the same place in all valid arragements
    const mapWithSameMines = mapMap(demapMap(mapArray));
    let thereIsTheSame = false;
    for (let i = 0; i < validArragements.length; i++) {
      runThroughMap((row, col) => {
        if (validArragements[i][row][col] === 'x') {
          if (mapWithSameMines[row][col] === '?' || mapWithSameMines[row][col].sameMines) {
            const sameMines = mapWithSameMines[row][col].sameMines || 0;
            mapWithSameMines[row][col] = {
              sameMines: sameMines + 1
            };
          }
        }
      });
    }
    runThroughMap((row, col) => {
      if (mapWithSameMines[row][col].sameMines === validArragements.length) {
        thereIsTheSame = true;
        mapArray[row][col] = 'x';
        minesSet++;
      } else if (mapWithSameMines[row][col] === '?') {
        thereIsTheSame = true;
        openPoint(row, col);
      }
    });

    if (LOG) console.log(demapMap(mapWithSameMines))

    return thereIsTheSame;

    function checkValidArragements() {
      for (let row = 0; row < mapArray.length; row++) {
        for (let col = 0; col < mapArray[0].length; col++) {
          if (mapCopy[row][col] === 'x' || mapCopy[row][col] === '?') {
            continue;
          }
          const pointsAround = doAround((row1, col1) => {
            return mapCopy[row1][col1];
          }, row, col);
          const minesAround = pointsAround.filter(point1 => point1 === 'x').length;
          if (mapCopy[row][col] != minesAround) {
            return false;
          }
        }
      }
      return true;
    }

    function getCombinations(array, count) {
      const combinations = [];
      
      if (count === 1) {
        for (let i = 0; i < array.length; i++) {
          combinations.push([array[i]]);
        }
        return combinations;
      }

      for (let i = 0; i < array.length; i++) {
        const combinations1 = getCombinations(array.slice(i + 1), count - 1);
        for (let j = 0; j < combinations1.length; j++) {
          combinations1[j].unshift(array[i]);
        }
        combinations.push(...combinations1);
      }

      return combinations;
    }

  }
  
}

console.log(solveMine(map, mines))
