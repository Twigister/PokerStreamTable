"use client";

import { useState, useEffect } from "react";
import { PlayerType } from "../types";
import PlayerWrapper from "./player/player_wrapper";
import styles from "./game.module.css"

export default function Game() {
  const [players, setPlayers] = useState<PlayerType[]>([]); 
  
  useEffect(() => {
    const apiData:PlayerType[] = [
      { id: 1, name: "Armand", cards: [{id: 1, rank: "A", suit: "h"}, {id: 2, rank: "K", suit: "h"}], stack: 1000 },
      { id: 2, name: "Max", cards: [{id: 1, rank: "J", suit: "d"}, {id: 2, rank: "7", suit: "d"}], stack: 30 },
      { id: 3, name: "Mehdi", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
      { id: 4, name: "Mireille", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
      { id: 5, name: "Mathieu", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
      { id: 6, name: "Mehdi", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
      { id: 7, name: "Mehdi", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
      { id: 8, name: "Mehdi", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
      { id: 9, name: "Mehdi", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
      { id: 10, name: "Mehdi", cards: [{id: 1, rank: "5", suit: "d"}, {id: 2, rank: "3", suit: "d"}], stack: 3000 },
    ]
    setPlayers(apiData);
  }, []);

  const updatePlayer = (updatedPlayer: PlayerType) => {
    console.log("Deez nuts");
    setPlayers((prev) => prev.map((p: PlayerType) => {
      if (p.id === updatedPlayer.id) {
        return {...p, ...updatedPlayer};
      } else
        return p;
    }));
    console.log(players);
  }

    return (
      <div className={styles.game}>
        <div className={styles.table}><span className={styles.game_name}>TONTON'S GAME</span></div>
        {players.map((p) => (<PlayerWrapper key={p.id} player={p} onPlayerUpdate={updatePlayer}/>))}
      </div>
    );
}
