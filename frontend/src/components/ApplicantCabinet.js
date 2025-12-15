import './styles/ApplicantCabinet.css';

const ApplicantCabinet = ({ onLogout, onStartNew }) => {
  return (
    <section className="cabinet-page">
      <header className="cabinet-header">
        <div>
          <h1>Платформа управления инновациями в здравоохранении</h1>
          <p className="muted">Личный кабинет заявителя</p>
        </div>
        <button type="button" className="secondary-btn" onClick={onLogout}>
          Выйти
        </button>
      </header>

      <div className="cabinet-summary">
        <div>
          <h2>Личный кабинет заявителя</h2>
          <p className="muted">ООО «МедИнновации» (ИНН: 7701234567)</p>
        </div>
        <div className="summary-counters">
          <div className="summary-card">
            <div className="summary-value">0</div>
            <div className="summary-label">Всего заявок</div>
          </div>
          <div className="summary-card">
            <div className="summary-value">0</div>
            <div className="summary-label">На рассмотрении</div>
          </div>
          <div className="summary-card">
            <div className="summary-value">0</div>
            <div className="summary-label">Одобрено</div>
          </div>
          <div className="summary-card summary-card--danger">
            <div className="summary-value">0</div>
            <div className="summary-label">Требует доработки</div>
          </div>
        </div>
        <div className="summary-actions">
          <button type="button" className="primary-btn" onClick={() => onStartNew && onStartNew()}>
            Создать новую заявку
          </button>
          <span className="muted small">Пока без сохранения, только макет формы</span>
        </div>
      </div>

      <section className="cabinet-block">
        <h3>Уведомления</h3>
        <div className="empty-block">У вас пока нет уведомлений.</div>
      </section>

      <section className="cabinet-block cabinet-block--danger">
        <h3>Отклонённые заявки — требуется доработка</h3>
        <div className="empty-block">У вас пока нет отклонённых заявок.</div>
      </section>

      <section className="cabinet-block">
        <h3>Все мои заявки</h3>
        <div className="empty-block">Вы ещё не подали ни одной заявки.</div>
      </section>

      <section className="cabinet-block">
        <h3>История уведомлений</h3>
        <div className="empty-block">История уведомлений появится после первых событий.</div>
      </section>

      <section className="cabinet-block">
        <h3>Документы</h3>
        <div className="empty-block">Документы будут доступны после принятия решений по заявкам.</div>
      </section>

      <section className="cabinet-block cabinet-help">
        <h3>Справка</h3>
        <ul>
          <li>Для создания новой заявки нажмите кнопку «Создать новую заявку».</li>
          <li>Заявки с красным статусом «Отклонено» можно будет доработать и подать повторно.</li>
          <li>Вы будете получать уведомления по email при изменении статуса заявки.</li>
          <li>Все решения и документы будут доступны в разделе «Документы».</li>
          <li>Для просмотра полной информации о заявке используйте действие «Просмотр».</li>
        </ul>
      </section>
    </section>
  );
};

export default ApplicantCabinet;

