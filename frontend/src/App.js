import { useMemo, useState } from 'react';
import RoleSelection from './components/RoleSelection';
import RegistrationForm from './components/RegistrationForm';
import ApplicantLogin from './components/ApplicantLogin';
import ApplicantCabinet from './components/ApplicantCabinet';
import ApplicationWizard from './components/ApplicationWizard';
import './App.css';

function App() {
  const [view, setView] = useState('roles'); // roles | registration | login | cabinet | application
  const apiBaseUrl = useMemo(() => process.env.REACT_APP_API_URL || 'http://localhost:8000', []);

  const handleLoggedIn = () => {
    setView('cabinet');
  };

  const handleLogout = async () => {
    try {
      await fetch(`${apiBaseUrl}/api/auth/logout`, { method: 'POST', credentials: 'include' });
    } catch {
      // ignore logout errors
    }
    setView('roles');
  };

  return (
    <div className="app-shell">
      {view === 'roles' && (
        <RoleSelection
          onSelectRegistration={() => setView('registration')}
          onSelectApplicant={() => setView('login')}
          onComingSoon={() => alert('Пока в разработке')}
        />
      )}
      {view === 'registration' && (
        <RegistrationForm apiBaseUrl={apiBaseUrl} onBack={() => setView('roles')} />
      )}
      {view === 'login' && (
        <ApplicantLogin apiBaseUrl={apiBaseUrl} onBack={() => setView('roles')} onLoggedIn={handleLoggedIn} />
      )}
      {view === 'cabinet' && <ApplicantCabinet onLogout={handleLogout} onStartNew={() => setView('application')} />}
      {view === 'application' && (
        <ApplicationWizard onBackToCabinet={() => setView('cabinet')} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;
