"use client";

import { useEffect } from "react";
import { PlayerType } from "../types";
import Player from "./player";
import PlayerControls from "./player_controls";
import styles from "./player_wrapper.module.css";

const player_positions = [
  { top: '5%', left: '50%', transform: 'translateX(-50%)' },   // top center
  { top: '5%', right: '250px' },                                  // top right
  { top: '20%', right: '20px' },                                  // middle right top
  { top: '55%', right: '20px' },                                  // middle right bottom
  { bottom: '5%', right: '250px' },                               // bottom right
  { bottom: '5%', left: '50%', transform: 'translateX(-50%)' }, // bottom center
  { bottom: '5%', left: '250px' },                                // bottom left
  { top: '55%', left: '20px' },                                   // middle left bottom
  { top: '20%', left: '20px' },                                   // middle left top
  { top: '5%', left: '250px' },                                   // top left
];

export default function PlayerWrapper({player, onPlayerUpdate}: {player: PlayerType, onPlayerUpdate: (updatedPlayer: PlayerType) => void}) {
  return (
    <div className={styles.player_wrapper} style={player_positions[player.id-1]}>
      <Player player={player}/>
      <PlayerControls player={player} onPlayerUpdate={onPlayerUpdate}/>
    </div>
  );
}