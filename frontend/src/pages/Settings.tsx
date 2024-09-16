import React, { useState } from 'react';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { updateUserSettings } from '@/services/api';
import { useAppSelector, useAppDispatch } from '@/store';
import { selectCurrentUser, updateUser } from '@/store/userSlice';

// HUMAN ASSISTANCE NEEDED
// The following component may need additional refinement for production readiness.
// Please review and adjust as necessary.

const Settings: React.FC = () => {
  const dispatch = useAppDispatch();
  const currentUser = useAppSelector(selectCurrentUser);
  const [name, setName] = useState(currentUser?.name || '');
  const [email, setEmail] = useState(currentUser?.email || '');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const updatedSettings = await updateUserSettings({ name, email });
      dispatch(updateUser(updatedSettings));
      // TODO: Add success message or notification
    } catch (error) {
      console.error('Failed to update settings:', error);
      // TODO: Add error handling and user feedback
    }
  };

  return (
    <div className="settings-page">
      <Header />
      <main>
        <h1>User Settings</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit">Save Settings</button>
        </form>
      </main>
      <Footer />
    </div>
  );
};

export default Settings;