// var ruyLopez = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
// var board = Chessboard('board', ruyLopez)
// var board2 = Chessboard('board2', ruyLopez)
// board2.move("a7-a6")

function loadBoard(lichess_id, blunder_fen, before_fen, orientation, move_uci, alternative_uci) {
    board_bl = $("#board_" + lichess_id + "_0")
    var game_blunder = new Chess(before_fen)
    blunder = game_blunder.move(move_uci, { sloppy: true })
    var config_blunder = {
        position: blunder_fen,
        orientation: orientation,
    }
    var board_blunder = Chessboard("board_" + lichess_id + "_0", config_blunder)
    board_bl.find(".square-" + blunder.from).addClass('highlight-red')
    board_bl.find(".square-" + blunder.to).addClass('highlight-red')

    board_alt = $("#board_" + lichess_id + "_1")
    var game_alternative = new Chess(before_fen)
    alternative = game_alternative.move(alternative_uci, { sloppy: true })
    var config_alternative = {
        position: game_alternative.fen(),
        orientation: orientation,
    }
    var board_alternative = Chessboard("board_" + lichess_id + "_1", config_alternative)
    board_alt.find(".square-" + alternative.from).addClass('highlight-green')
    board_alt.find(".square-" + alternative.to).addClass('highlight-green')

    $(window).resize(function(){
        board_blunder.resize()
        board_alternative.resize()
        // $("#board_" + lichess_id + "_0").find(".square-" + blunder.from).addClass('highlight-red')
        // $("#board_" + lichess_id + "_0").find(".square-" + blunder.to).addClass('highlight-red')
        // $("#board_" + lichess_id + "_1").find(".square-" + alternative.from).addClass('highlight-green')
        // $("#board_" + lichess_id + "_1").find(".square-" + alternative.to).addClass('highlight-green')
    })
}