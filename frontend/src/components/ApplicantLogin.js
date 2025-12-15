import { useState } from 'react';
import './styles/ApplicantLogin.css';

const ApplicantLogin = ({ apiBaseUrl, onBack, onLoggedIn }) => {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!login || !password) {
      setError('Введите логин и пароль');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${apiBaseUrl}/api/auth/login`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password }),
      });
      if (!res.ok) {
        const msg = (await res.json().catch(() => ({}))).detail || 'Неверный логин или пароль';
        throw new Error(msg);
      }
      await res.json(); // можем не использовать, просто убедиться, что ответ корректный
      onLoggedIn?.();
    } catch (e) {
      setError(e.message || 'Ошибка авторизации, попробуйте ещё раз');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="login-page">
      <div className="login-card">
        <h1 className="login-title">Платформа управления инновациями в здравоохранении</h1>
        <p className="login-subtitle">Вход для претендентов</p>
        <form className="login-form" onSubmit={handleSubmit}>
          <label>
            Логин (email)
            <input
              type="email"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              placeholder="ivanov@medinnovations.ru"
            />
          </label>
          <label>
            Пароль
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Введите пароль"
            />
          </label>
          {error && <div className="status-message error">{error}</div>}
          <div className="login-actions">
            <button type="button" className="secondary-btn" onClick={onBack}>
              Назад
            </button>
            <button type="submit" className="primary-btn" disabled={loading}>
              {loading ? 'Входим...' : 'Войти'}
            </button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default ApplicantLogin;

