from multiprocessing.sharedctypes import Value
from typing import List
import io

import chess
import chess.pgn

from lyre.analysis import AnalysedGame


def opening_tree(games: List[AnalysedGame], skip_blunders: bool = False, threshold: int = -200) -> chess.pgn.Game:
    white: List[AnalysedGame] = []
    black: List[AnalysedGame] = []
    for game in games:
        if game.colour_player == "white":
            white.append(game)
        else:
            black.append(game)
    
    white_openings = []
    black_openings = []
    
    for game in white:
        moves: List[chess.Move] = [] 
        for i in range(6):
            try:
                move = game.moves[i]
            except IndexError:
                break
            if move.score_delta < threshold:
                if not skip_blunders:
                    moves.append(chess.Move.from_uci(move.engine_lines[0].sequence[0]))
                break
            else:
                moves.append(chess.Move.from_uci(move.move))
                try:
                    moves.append(chess.Move.from_uci(move.move_after))
                except ValueError:
                    break
        opening = chess.pgn.Game()
        opening.add_line(moves)
        white_openings.append(opening)
    
    for game in black:
        moves: List[chess.Move] = [] 
        for i in range(6):
            try:
                move = game.moves[i]
            except IndexError:
                break
            try:
                moves.append(chess.Move.from_uci(move.move_before))
            except ValueError:
                break
            if move.score_delta < threshold:
                if not skip_blunders:
                    moves.append(chess.Move.from_uci(move.engine_lines[0].sequence[0]))
                break
            else:
                moves.append(chess.Move.from_uci(move.move))
        opening = chess.pgn.Game()
        opening.add_line(moves)
        black_openings.append(opening)
    
    white_repertoire = combine_games(white_openings)
    black_repertoire = combine_games(black_openings)
    
    return (white_repertoire, black_repertoire)


def combine_games(games: List[chess.pgn.Game]) -> chess.pgn.Game:
    master_node = chess.pgn.Game()

    mlist = []
    for game in games:
        mlist.extend(game.variations)

    variations = [(master_node, mlist)]
    done = False

    while not done:
        newvars = []
        done = True
        for vnode, nodes in variations:
            newmoves = {}
            for node in nodes:
                if node.move is None:
                    continue
                elif node.move not in list(newmoves):
                    nvnode = vnode.add_variation(node.move)
                    if len(node.variations) > 0:
                        done = False
                    newvars.append((nvnode, node.variations))
                    newmoves[node.move] = len(newvars) - 1
                else:
                    nvnode, nlist = newvars[newmoves[node.move]]
                    if len(node.variations) > 0:
                        done = False
                    nlist.extend(node.variations)
                    newvars[newmoves[node.move]] = (nvnode, nlist)
        variations = newvars
    
    return master_node