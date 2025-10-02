"use client";

import { useState, useEffect } from "react";
import { PlayerType } from "../types";
import PlayerWrapper from "./player_wrapper";
import LeBouton from "./le_bouton_qui_sent_bon";

export default function Game() {
  const [players, setPlayers] = useState<PlayerType[]>([]); 
  
  useEffect(() => {
    const apiData = [
      { id: 1, name: "Armand", cards: [{id: 1, rank: "A", suit: "h"}, {id: 2, rank: "K", suit: "h"}] },
      { id: 2, name: "Max", cards: [{id: 1, rank: "J", suit: "d"}, {id: 2, rank: "7", suit: "d"}]}
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
      <div>
        {players.map((p) => (<PlayerWrapper key={p.id} player={p} onPlayerUpdate={updatePlayer}/>))}
        <LeBouton/>
      </div>
    );
}
