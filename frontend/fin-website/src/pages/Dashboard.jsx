import "./layouts/Home.css";

function Dashboard() {

  // Fazer lógica para que, se o usuário não tiver nenhum portifólio, dexar um botão em azul no meio da tela para que ele possa criar um portifólio
  // e, se o usuário já tiver um portifólio, mostrar os portifólios que ele tem com um botão para cada portifólio que o usuário tem.

  return (
    <div className="home-container">
      <header>
        <h1>Portifolios</h1>
      </header>
      <main className="main-content"></main>
    </div>
  );
}

export default Dashboard;
