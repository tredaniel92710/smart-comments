import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';
import PostList from './components/PostList';
import PostDetail from './components/PostDetail';
import ModeratorView from './components/ModeratorView';

function Navigation() {
  const location = useLocation();
  
  return (
    <nav>
      <Link
        to="/"
        className={location.pathname === '/' ? 'active' : ''}
      >
        Posts
      </Link>
      <Link
        to="/moderator"
        className={location.pathname === '/moderator' ? 'active' : ''}
      >
        Moderator View
      </Link>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <header className="App-header">
          <h1>
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              Smart Comments
            </Link>
          </h1>
          <Navigation />
        </header>
        <main>
          <Routes>
            <Route path="/" element={<PostList />} />
            <Route path="/posts/:id" element={<PostDetail />} />
            <Route path="/moderator" element={<ModeratorView />} />
          </Routes>
        </main>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
      </div>
    </BrowserRouter>
  );
}

export default App;
