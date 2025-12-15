import { useMemo, useState } from 'react';
import './styles/RegistrationForm.css';

const RegistrationForm = ({ apiBaseUrl, onBack }) => {
  const [emailLocal, setEmailLocal] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const emailDomain = useMemo(() => '@medinnovations.ru', []);

  const isValidLocal = (value) => /^[a-zA-Z0-9._-]+$/.test(value);

  const handleSubmit = async () => {
    const login = `${emailLocal}${emailDomain}`.trim();
    if (!emailLocal) {
      setError('Введите локальную часть email');
      return;
    }
    if (!isValidLocal(emailLocal)) {
      setError('Допустимы только латинские буквы, цифры и символы . _ -');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const res = await fetch(`${apiBaseUrl}/api/auth/register`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nickname: login, create_if_missing: true }),
      });
      if (!res.ok) {
        const msg = (await res.json().catch(() => ({}))).detail || 'Не удалось зарегистрироваться';
        throw new Error(msg);
      }
      const data = await res.json();
      const shownLogin = data.login || login;
      alert(`Успешная регистрация.\nЛогин: ${shownLogin}\nПароль: ${shownLogin}`);
      onBack?.();
    } catch (e) {
      setError(e.message || 'Ошибка регистрации, попробуйте ещё раз');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="registration-page">
      <div className="reg-header">
        <h1>Платформа управления инновациями в здравоохранении</h1>
        <p className="reg-subtitle">Регистрация организации</p>
      </div>

      <div className="reg-card">
        <div className="reg-card__head">
          <button className="back-btn" type="button" onClick={onBack}>
            ← Назад
          </button>
          <div>
            <h2>Регистрация организации</h2>
            <p className="muted">Заполните данные вашей организации (7 полей)</p>
          </div>
        </div>

        <div className="reg-form">
          <div className="form-group">
            <label>Общая информация по проекту</label>
            <p className="muted">Информация о претенденте и контактном лице</p>
            <p className="muted small">Поля, отмеченные звездочкой (*), обязательны для заполнения</p>
          </div>

          <div className="form-group">
            <label>Наименование юридического лица (в соответствии с уставными документами)*</label>
            <input type="text" placeholder="ООО «МедИнновации»" disabled />
          </div>
          <div className="form-group">
            <label>Наименование юридического лица (на английском языке)</label>
            <input type="text" placeholder="Medinnovations LLC" disabled />
          </div>
          <div className="form-group">
            <label>ИНН юридического лица*</label>
            <input type="text" placeholder="7701234567" disabled />
          </div>
          <div className="form-group">
            <label>Руководитель юридического лица, его контактные данные (электронная почта, телефон)*</label>
            <input type="text" placeholder="Петров Петр Петрович, petrov@medinnovations.ru, +7 (999) 111-22-33" disabled />
          </div>
          <div className="form-group">
            <label>Контактное лицо для взаимодействия (ФИО, должность)*</label>
            <input type="text" placeholder="Иванов Иван Иванович, Руководитель отдела развития" disabled />
          </div>
          <div className="form-group">
            <label>Телефон контактного лица*</label>
            <input type="text" placeholder="+7 (999) 123-45-67" disabled />
          </div>
          <div className="form-group">
            <label>Электронная почта контактного лица*</label>
            <div className="email-row">
              <input
                type="text"
                value={emailLocal}
                onChange={(e) => setEmailLocal(e.target.value)}
                placeholder="ivanov"
              />
              <span className="email-domain">{emailDomain}</span>
            </div>
            <p className="muted small">Логин и пароль будут: {emailLocal || '...'}{emailDomain}</p>
          </div>
        </div>

        {error && <div className="status-message error">{error}</div>}

        <div className="reg-actions">
          <button className="primary-btn" type="button" onClick={handleSubmit} disabled={loading}>
            {loading ? 'Сохраняем...' : 'Зарегистрироваться'}
          </button>
        </div>
      </div>

      <div className="reg-info">
        <h3>Информация о регистрации</h3>
        <ul>
          <li>После регистрации вам будет отправлено письмо с подтверждением на указанный email</li>
          <li>Эти данные будут автоматически использованы во всех ваших заявках</li>
          <li>ИНН проверяется автоматически через ЕГРЮЛ API</li>
          <li>Организация должна быть действующей, не в процессе ликвидации и не офшорной</li>
        </ul>
      </div>
    </section>
  );
};

export default RegistrationForm;
