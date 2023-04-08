// ==UserScript==
// @name         Lichess Cheat Undetected
// @namespace    https://www.example.com/
// @version      1.0
// @description  Provides the best move in Lichess without being detected and without exceeding 80% accuracy in chess.
// @author       DUDE
// @match        https://lichess.org/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    var accuracyThreshold = 80;

    var chessboard = document.querySelector('.cg-board');

    var observeDOM = (function(){
        var MutationObserver = window.MutationObserver || window.WebKitMutationObserver,
            eventListenerSupported = window.addEventListener;

        return function(obj, callback){
            if( MutationObserver ){
                var obs = new MutationObserver(function(mutations, observer){
                    if( mutations[0].addedNodes.length || mutations[0].removedNodes.length )
                        callback();
                });
                obs.observe( obj, { childList:true, subtree:true });
            }
            else if( eventListenerSupported ){
                obj.addEventListener('DOMNodeInserted', callback, false);
                obj.addEventListener('DOMNodeRemoved', callback, false);
            }
        };
    })();

    observeDOM(chessboard, function(){
        var fen = document.querySelector('.cg-board .cg-wrap .cg-fen').textContent.trim();
        var skillLevel = Math.floor(Math.random() * (100 - accuracyThreshold + 1)) + accuracyThreshold;
        var requestURL = 'https://explorer.lichess.ovh/lichess?fen=' + fen + '&topGames=' + skillLevel + '&variant=standard';

        var xhr = new XMLHttpRequest();
        xhr.open('GET', requestURL, true);
        xhr.onload = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var bestMove = response.moves[0];

                var event = new CustomEvent('lichessmove', { detail: { from: bestMove.from, to: bestMove.to, promotion: bestMove.promotion }});
                document.dispatchEvent(event);
            }
        };
        xhr.send();
    });
})();
