/* jshint esversion: 11 */

const SCALE = 4;
const SPEED = 60;
const FRAME_STEPS = 10000; // How much steps are simulate per frame

const SIDE_SPACE = 100; // How much fields to show around the original grid

let final_frame = false; // Flag - final frame should be rendered

let lines;
let grid = [];

let sand_stable_cnt = 0;

const SAND_SOURCE = [500, 0];
let sand_active = [...SAND_SOURCE];

// Init values from sand generator
let grid_x_min = 500;
let grid_x_max = 500;
let grid_y_min = 0;
let grid_y_max = 0;

const ROCK = 'R';
const SAND = 'S';

function add_lines(points) {
  let previous;
  let next;
  for (let idx in points) {
    previous = next;
    next = points[idx].split(',').map(str => Number(str));
    if (!previous) {
      // Initialize loop
      // grid_x_min = grid_x_min ?? next[0];
      // grid_x_max = grid_x_max ?? next[0];
      // grid_y_min = grid_y_min ?? next[1];
      // grid_y_max = grid_y_max ?? next[1];
      continue;
    }

    // Draw the line as a rect with one dimesion = 1 field only
    let x_from = min(previous[0], next[0]);
    let x_to   = max(previous[0], next[0]);

    let y_from = min(previous[1], next[1]);
    let y_to   = max(previous[1], next[1]);

    // Update min/max indexes
    grid_x_min = min(x_from, grid_x_min);
    grid_x_max = max(x_to,   grid_x_max);
    grid_y_min = min(y_from, grid_y_min);
    grid_y_max = max(y_to,   grid_y_max);

    for (let x = x_from; x <= x_to; x++) {
      // grid should be 2D array, but I do not know indexes of inner arrays beforehands
      // Need to create each array in 2nd dimension on demand
      if (!Array.isArray(grid[x])) {
        grid[x] = [];
      }
      for (let y = y_from; y <= y_to; y++) {
        // Fill the line in grid
        grid[x][y] = ROCK;
      }
    }
  }
}

function preload() {
  // preload() is a starting point of this program
  // this loads lines form input file

  lines = loadStrings('input_day_14.txt');
  // lines = loadStrings('input_test.txt');

  // setup() runs automatically after this
}

function setup() {
  // setup() runs after preload() and has preloaded data available
  // this runs just once and should prepare everything for the draw() loop

  console.log('Input lines count: ' + lines.length);

  for (let idx in lines) {
    let ln = lines[idx];
    let points = ln.split(' -> ');
    add_lines(points);
  }

  // console.log('X from ' + grid_x_min + ' to ' + grid_x_max
  //             + ' / Y from ' + grid_y_min + ' to ' + grid_y_max);

  // Setup drawing canvas
  createCanvas(
    (grid_x_max - grid_x_min + 3 + SIDE_SPACE * 2) * SCALE,
    (grid_y_max - grid_y_min + 3 + 2) * SCALE
  );
  frameRate(SPEED);

  // draw() runs automatically after this
}

function draw_field(grid_x, grid_y, sand_override=false, force_rock=false) {
  // Compute graphics coordinates of grid field
  let x = (grid_x - grid_x_min + 1 + SIDE_SPACE) * SCALE;
  let y = (grid_y - grid_y_min + 1) * SCALE;
  let size = 1 * SCALE;

  // Setup drawing style
  if (force_rock || (grid[grid_x] && grid[grid_x][grid_y] == ROCK)) {
    stroke(0);
    fill(64);
  }
  else if (grid[grid_x] && grid[grid_x][grid_y] == SAND) {
    stroke(240, 180, 100);
    fill(240, 200, 100);
  }
  else if (!sand_override) {
    // Empty
    return;
  }

  if (sand_override) {
    stroke(240, 80, 40);
    fill(240, 200, 100);
  }

  rect(x, y, size, size);
}

function draw_sand() {
  draw_field(sand_active[0], sand_active[1], true);
}

function move_sand() {
  let sand_x = sand_active[0];
  let sand_y = sand_active[1];

  let next_sand = false;

  // Sand on the ground
  // set stable and continue with next
  if (sand_y > grid_y_max) {
    next_sand = true;
  }

  if (!next_sand) {
    // move down
    if (!grid[sand_x] || !grid[sand_x][sand_y + 1]) {
      sand_active[1]++;
      return;
    }
    // move left down
    else if (!grid[sand_x - 1] || !grid[sand_x - 1][sand_y + 1]) {
      sand_active[0]--;
      sand_active[1]++;
      return;
    }
    // move right down
    else if (!grid[sand_x + 1] || !grid[sand_x + 1][sand_y + 1]) {
      sand_active[0]++;
      sand_active[1]++;
      return;
    }
    else {
      next_sand = true;
    }
  }

  // stop movement, start next
  if (next_sand) {
    // Set stable sand in grid
    sand_stable_cnt++;
    if (!Array.isArray(grid[sand_x])) {
      grid[sand_x] = [];
    }
    grid[sand_x][sand_y] = SAND;

    // If this is the source field, end simulation
    if (sand_x == SAND_SOURCE[0] && sand_y == SAND_SOURCE[1]) {
      // Print result
      console.log('Stable sand count: ' + sand_stable_cnt);
      // Stop simulation
      noLoop();
      final_frame = true;
      draw();
      return;
    }

    // Create new sand
    sand_active = [...SAND_SOURCE];
  }
}

function draw() {
  // draw() is a rendering loop
  // this runs after setup() and is repeated automatically
  // each run is delayed after the previous to ensure stable frame rate
  // each run should render one frame

  // Prepare new frame
  background(140);
  // strokeCap(PROJECT);
  // strokeJoin(MITER);

  for (let x in grid) {
    let col = grid[x];
    for (let y in col) {
      // let field = col[y];
      draw_field(x, y);
    }
  }

  // Draw the floor line
  for (let x = grid_x_min - SIDE_SPACE - 1; x <= grid_x_max + SIDE_SPACE + 1; x++) {
    draw_field(x, grid_y_max + 2, false, true);
  }

  draw_sand();
  if (final_frame) {
    return;
  }

  for (let idx = 0; idx < FRAME_STEPS; idx++) {
    move_sand();
    if (final_frame) {
      break;
    }
  }
}
