/**
 * Render the profile settings form and submit it.
 *
 * Three imported names do not exist: `updateUserSettings` in `@/services/api`, and
 * `selectCurrentUser` and `updateUser` in the user slice. `Header` and `Footer` are
 * imported by name and both are default exports. See the HUMAN ASSISTANCE NEEDED
 * marker below.
 *
 * @see ./README.md
 */
import React, { useState } from 'react';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { updateUserSettings } from '@/services/api';
import { useAppSelector, useAppDispatch } from '@/store';
import { selectCurrentUser, updateUser } from '@/store/userSlice';

// HUMAN ASSISTANCE NEEDED
// The following component may need additional refinement for production readiness.
// Please review and adjust as necessary.

/**
 * Render a controlled two-field form for the display name and the email address.
 *
 * Both fields initialise from `currentUser` once, when the component first renders.
 * `currentUser` starts as `null`, so a profile that arrives later leaves the form
 * empty. The name field reads `currentUser?.name`, and no user contract declares a
 * `name` field. The markup carries no class names at all, so the form is unstyled
 * under either convention in the tree.
 *
 * @returns The settings page element.
 */
const Settings: React.FC = () => {
  const dispatch = useAppDispatch();
  const currentUser = useAppSelector(selectCurrentUser);
  const [name, setName] = useState(currentUser?.name || '');
  const [email, setEmail] = useState(currentUser?.email || '');

  /**
   * Submit the form and store the updated profile.
   *
   * @param e - The form submit event, whose default is prevented so the page does
   * not reload.
   * @returns A promise that resolves once the update settles. Failures are logged
   * to the console and nothing tells the reader. See the two TODO markers inside.
   */
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