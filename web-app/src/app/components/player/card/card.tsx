import { CardType } from "../types";
import styles from "./card.module.css"

export default function Card({data}: {data: CardType}) {
  let hIndex = "A23456789TJQK".indexOf(data.rank);
  let vIndex = "hdsc".indexOf(data.suit);

  if (vIndex === -1 || hIndex === -1) {
    vIndex = 4;
    hIndex = 0;
  }

  return (
    <div className={styles.card} style={{backgroundPosition: `-${hIndex * 48}px -${vIndex * 64}px`}}></div>
  );
};