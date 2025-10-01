"use client";

import { useEffect } from "react";
import { PlayerType } from "../types";
import Player from "./player";
import PlayerControls from "./playercontrols";

export default function PlayerWrapper({player, onPlayerUpdate}: {player: PlayerType, onPlayerUpdate: (updatedPlayer: PlayerType) => void}) {
  return (
    <div className="PlayerWrapper">
      <Player player={player} onPlayerUpdate={onPlayerUpdate}/>
      <PlayerControls player={player} onPlayerUpdate={onPlayerUpdate}/>
    </div>
  );
}