import './styles/RoleSelection.css';

const roles = [
  {
    id: 'candidate',
    title: 'Новый претендент',
    subtitle: 'Регистрация организации',
    icon: '👤➕',
    color: '#1e6bff',
  },
  {
    id: 'applicant',
    title: 'Претендент',
    subtitle: 'Подача и отслеживание заявок',
    icon: '🏢',
    color: '#1e6bff',
  },
  {
    id: 'admin',
    title: 'Администратор',
    subtitle: 'Принятие решений по заявкам',
    icon: '🛠️',
    color: '#0faf63',
  },
  {
    id: 'expert',
    title: 'Эксперт',
    subtitle: 'Экспертная оценка проектов',
    icon: '🧑‍💼',
    color: '#a020f0',
  },
  {
    id: 'manager',
    title: 'Управленец',
    subtitle: 'Аналитика и общая картина',
    icon: '📊',
    color: '#f25c05',
  },
];

const RoleSelection = ({ onSelectRegistration, onSelectApplicant, onComingSoon }) => {
  return (
    <section className="role-section">
      <div className="role-hero">
        <h1>Единая платформа управления цифровыми инновационными проектами в здравоохранении</h1>
        <p>Выберите роль для входа в систему</p>
      </div>

      <div className="role-grid">
        {roles.map((role) => {
          const isPrimary = role.id === 'candidate';
          return (
            <button
              key={role.id}
              className={`role-card ${isPrimary ? 'role-card--primary' : ''}`}
              onClick={() => {
                if (role.id === 'candidate') {
                  onSelectRegistration?.();
                } else if (role.id === 'applicant') {
                  onSelectApplicant?.();
                } else {
                  onComingSoon?.();
                }
              }}
              type="button"
            >
              <div className="role-icon" style={{ color: role.color }}>
                {role.icon}
              </div>
              <div className="role-text">
                <h3>{role.title}</h3>
                <p>{role.subtitle}</p>
              </div>
            </button>
          );
        })}
      </div>
    </section>
  );
};

export default RoleSelection;
