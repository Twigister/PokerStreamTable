import Game from "./components/game";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.header_links}>
          <span>Link 1</span>
          <span>Link 2</span>
          <span>Link 3</span>
        </div>
        <button className={styles.settings}></button>
      </header>
      <Game/>
      <footer className={styles.footer}>
        On touche le fond..
      </footer>
    </div>
  );
}
