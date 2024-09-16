import React from 'react';
import { Link } from 'react-router-dom';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

const Home: React.FC = () => {
  const currentUser = useAppSelector(selectCurrentUser);

  return (
    <div className="home-container">
      <Header />
      <main className="home-content">
        <h1>Welcome to Microsoft Word</h1>
        {currentUser && <p>Hello, {currentUser.name}!</p>}
        <div className="quick-access">
          <Link to="/new-document" className="quick-access-button">
            New Document
          </Link>
          <Link to="/open-document" className="quick-access-button">
            Open Document
          </Link>
          <Link to="/recent-documents" className="quick-access-button">
            Recent Documents
          </Link>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Home;