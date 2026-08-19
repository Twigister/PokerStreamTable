"use client";

import { useDrop } from "react-dnd";
import { PlayerType } from "../types";
import Player from "./player";
import PlayerControls from "./player_controls";
import styles from "./player_wrapper.module.css";
import { PLAYER_DRAG_TYPE } from "../../types";

const player_positions = [
  { top: '1%', left: '50%', transform: 'translateX(-50%)' },      // top center
  { top: '1%', right: '250px' },                                  // top right
  { top: '20%', right: '10px' },                                  // middle right top
  { top: '55%', right: '10px' },                                  // middle right bottom
  { bottom: '1%', right: '250px' },                               // bottom right
  { bottom: '1%', left: '50%', transform: 'translateX(-50%)' },  // bottom center
  { bottom: '1%', left: '250px' },                                // bottom left
  { top: '55%', left: '10px' },                                   // middle left bottom
  { top: '20%', left: '10px' },                                   // middle left top
  { top: '1%', left: '250px' },                                   // top left
];

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function PlayerWrapper({
  player,
  seatNumber,
  onPlayerUnseated,
  onPlayerSeated,
}: {
  player: PlayerType | null;
  seatNumber: number;
  onPlayerUnseated: (playerId: number) => void;
  onPlayerSeated: (updatedPlayer: PlayerType) => void;
}) {
  const [{ isOver, canDrop }, drop] = useDrop(() => ({
    accept: PLAYER_DRAG_TYPE,
    canDrop: (draggedPlayer: PlayerType) => !player && draggedPlayer.seat_number !== seatNumber,
    drop: async (draggedPlayer: PlayerType) => {
      try {
        const response = await fetch(`${API_URL}/users/seat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: draggedPlayer.id, table_id: 1, seat_number: seatNumber }),
        });

        if (!response.ok) {
          throw new Error("Unable to seat player.");
        }

        onPlayerSeated(await response.json());
      } catch (error) {
        window.alert((error as Error).message);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  }), [player, seatNumber, onPlayerSeated]);

  if (player) {
    return (
      <div ref={drop} className={styles.player_wrapper} style={player_positions[seatNumber - 1]}>
        <Player player={player}/>
        <PlayerControls player={player} onUnseat={onPlayerUnseated}/>
      </div>
    );
  }

  return (
    <div
      ref={drop}
      className={`${styles.player_wrapper} ${styles.empty_seat} ${isOver && canDrop ? styles.seat_highlight : ""}`}
      style={player_positions[seatNumber - 1]}
    >
      <span>Seat {seatNumber}</span>
      <span className={styles.empty_seat_label}>Drop player here</span>
    </div>
  );
}