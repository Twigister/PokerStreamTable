"use client";

import { useState, useEffect } from "react";
import { PlayerProfileUpdate, PlayerType, PlayerUnseatUpdate, SeatedPlayerUpdate } from "../types";
import PlayerWrapper from "./player/player_wrapper";
import styles from "./game.module.css"

export default function Game({
  updatedPlayer,
  onPlayerSeated,
  onPlayerUnseated,
}: {
  updatedPlayer: PlayerProfileUpdate | null;
  onPlayerSeated: (player: SeatedPlayerUpdate) => void;
  onPlayerUnseated: (player: PlayerUnseatUpdate) => void;
}) {
  const [players, setPlayers] = useState<(PlayerType | null)[]>(Array(10).fill(null));
  
  useEffect(() => { // Doit faire une requête à l'API pour récupérer les joueurs seat à la table et les mettre dans le state players
    async function fetchPlayers() {
      console.log("Mes fesses");
      const apiData:(PlayerType | null)[] = await (await fetch("http://127.0.0.1:8000/users/getTableState")).json();

      console.log(apiData);
      console.log("API DATA");
      setPlayers(apiData);
      return apiData;
    }
    fetchPlayers();
  }, []);

  useEffect(() => {
    if (!updatedPlayer) {
      return;
    }

    setPlayers((prev) => prev.map((player) => {
      if (player && player.id === updatedPlayer.id) {
        return { ...player, name: updatedPlayer.name, image_url: updatedPlayer.image_url };
      }
      return player;
    }));
  }, [updatedPlayer]);

  const unseatPlayer = (playerId: number) => {
    setPlayers((prev) => prev.map((player) =>
      player?.id === playerId ? null : player,
    ));
    onPlayerUnseated({ id: playerId });
  };

  const seatPlayer = (player: PlayerType) => {
    setPlayers((prev) => prev.map((seat, index) =>
      index === player.seat_number - 1 ? player : seat,
    ));
    onPlayerSeated({
      id: player.id,
      name: player.name,
      image_url: player.image_url ?? null,
      seat_number: player.seat_number,
    });
  };

    return (
      <div className={styles.game}>
        <div className={styles.table}><span className={styles.game_name}>TONTON'S GAME</span></div>
        {players.map((p, index) => (
          <PlayerWrapper
            key={p?.id ?? `empty-seat-${index + 1}`}
            player={p}
            seatNumber={index + 1}
            onPlayerUnseated={unseatPlayer}
            onPlayerSeated={seatPlayer}
          />
        ))}
      </div>
    );
}
