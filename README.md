# sudoku-python-tools

### Puzzle Generation

The current workflow is to first generate a large number of 28-known puzzles
relatively cheaply, using multiproc_puzzle_generator. This pre-generates a 
shuffled list of cells to remove, and removes them one by one, testing for 
uniqueness (and thus for a solvable puzzle too) after each removal. This process
terminates when an invalid puzzle is found, or the threshold known count is 
reached.

The second step is to take each of these puzzles, and using multiprocess_bleed_it_dry,
remove *every* possible digit, exploring all pathways. A dictionary keyed by 
known_count is kept for each, and the minimum key is taken if the target known
count is not hit. 23 seems to be a good balance point between ease of mining and
human solvability here. 22's are rare.

The third step is to take each of the 23-known puzzles and check them for human
solvability. Approx half of them pass this test. Ideally puzzles would be stored along
with a couple of booleans indicating which class of algorithms are necessary to solve
them, to allow them to be categorized according to difficulty level.

A basic correlation analysis was carried out across a range of metrics, and the strongest correlation was between the standard deviation of the count of known cells 
in each nonet, at 0.15. This doesn't seem like strong enough evidence to begin
generating puzzles under a strategy of distributing the knowns evenly across nonets, so
I'm continuing to generate the puzzles randomly.

This process is producting plenty of results, and with the ability to transform the 
puzzles using digit and nonet swapping, there will be plenty of puzzles for the app.
