import { useState } from 'react';
import './styles/ApplicationWizard.css';

const steps = [
  { id: 1, title: 'Информация о претенденте' },
  { id: 2, title: 'Информация о цифровой инновации' },
  { id: 3, title: 'Характеристики инновации' },
];

const ApplicationWizard = ({ onBackToCabinet, onLogout }) => {
  const [step, setStep] = useState(1);

  const renderStepContent = () => {
    if (step === 1) {
      return (
        <>
          <div className="wizard-subgroup">
            <h4>Группа 1. Общая информация по проекту</h4>
            <p className="muted small">Подгруппа I. Информация о претенденте (автозаполнение из регистрации)</p>
          </div>
          <div className="wizard-grid">
            <div className="wizard-field">
              <label>Наименование юридического лица*</label>
              <div className="wizard-field-readonly">ООО «МедИнновации»</div>
            </div>
            <div className="wizard-field">
              <label>Наименование (на английском языке)</label>
              <div className="wizard-field-readonly">MedInnovations LLC</div>
            </div>
            <div className="wizard-field">
              <label>ИНН юридического лица*</label>
              <div className="wizard-field-readonly">7701234567</div>
            </div>
            <div className="wizard-field">
              <label>Контактное лицо (ФИО, должность)*</label>
              <div className="wizard-field-readonly">Иванов Иван Иванович, Генеральный директор</div>
            </div>
            <div className="wizard-field">
              <label>Телефон контактного лица*</label>
              <div className="wizard-field-readonly">+7 (999) 123-45-67</div>
            </div>
            <div className="wizard-field">
              <label>Электронная почта контактного лица*</label>
              <div className="wizard-field-readonly">ivanov@medinnovations.ru</div>
            </div>
          </div>
        </>
      );
    }

    if (step === 2) {
      return (
        <>
          <div className="wizard-subgroup">
            <h4>Подгруппа II. Информация о цифровой инновации</h4>
          </div>
          <div className="wizard-grid">
            <div className="wizard-field">
              <label>Наименование цифровой инновации*</label>
              <div className="wizard-field-readonly">Система ИИ‑диагностики онкологии по КТ</div>
            </div>
            <div className="wizard-field">
              <label>Наименование (на английском языке)</label>
              <div className="wizard-field-readonly">AI Oncology CT Diagnosis System</div>
            </div>
            <div className="wizard-field wizard-field--full">
              <label>Краткое описание (&lt;1000 символов)*</label>
              <div className="wizard-field-readonly">
                Инновационная система анализа КТ‑исследований с использованием методов машинного обучения для раннего выявления
                онкологических заболеваний.
              </div>
            </div>
            <div className="wizard-field wizard-field--full">
              <label>Проблема, которую решает инновация (&lt;2000 символов)*</label>
              <div className="wizard-field-readonly">
                Поздняя диагностика опухолей, высокая нагрузка на врачей‑рентгенологов, необходимость повышения точности и
                скорости интерпретации КТ.
              </div>
            </div>
          </div>
        </>
      );
    }

    return (
      <>
        <div className="wizard-subgroup">
          <h4>Группа 2. Характеристики инновации</h4>
        </div>
        <div className="wizard-grid">
          <div className="wizard-field">
            <label>Наличие аналогов*</label>
            <div className="wizard-field-readonly">Имеются зарубежные аналоги</div>
          </div>
          <div className="wizard-field">
            <label>Потребительские преимущества*</label>
            <div className="wizard-field-readonly">Сокращение времени диагностики, повышение точности и воспроизводимости.</div>
          </div>
          <div className="wizard-field">
            <label>Степень зрелости (УГТ)*</label>
            <div className="wizard-field-readonly">Пилотная эксплуатация</div>
          </div>
          <div className="wizard-field">
            <label>Локализация производства*</label>
            <div className="wizard-field-readonly">Российская Федерация</div>
          </div>
          <div className="wizard-field">
            <label>Интеграция с МИС</label>
            <div className="wizard-field-readonly">Интеграция через стандарт HL7/FHIR</div>
          </div>
          <div className="wizard-field wizard-field--full">
            <label>Ожидаемый экономический результат*</label>
            <div className="wizard-field-readonly">
              Сокращение числа повторных исследований и экономия рабочего времени специалистов.
            </div>
          </div>
          <div className="wizard-field wizard-field--full">
            <label>Ожидаемые клинические эффекты*</label>
            <div className="wizard-field-readonly">
              Повышение доли ранних стадий выявления онкологических заболеваний, снижение доли пропущенных случаев.
            </div>
          </div>
        </div>
      </>
    );
  };

  const renderHelp = () => (
    <section className="wizard-help">
      <h3>Справка по заполнению</h3>
      <ul>
        <li>Поля, отмеченные звездочкой (*), обязательны для заполнения.</li>
        <li>Система автоматически сохраняет черновик каждые 5 минут.</li>
        <li>Вы можете вернуться к заполнению заявки в любое время.</li>
        <li>После отправки заявка получит уникальный номер и будет направлена на рассмотрение.</li>
        <li>Презентационные материалы должны включать сравнение с конкурентами, описание процессов, выгоды и затраты.</li>
      </ul>
    </section>
  );

  return (
    <section className="wizard-page">
      <header className="cabinet-header">
        <div>
          <h1>Платформа управления инновациями в здравоохранении</h1>
          <p className="muted">Личный кабинет заявителя</p>
        </div>
        <button type="button" className="secondary-btn" onClick={onLogout}>
          Выйти
        </button>
      </header>

      <div className="wizard-card">
        <div className="wizard-head">
          <button type="button" className="back-btn" onClick={onBackToCabinet}>
            ← Назад в личный кабинет
          </button>
          <div>
            <h2>Создание новой заявки</h2>
            <p className="muted">Заполните все обязательные поля (*)</p>
          </div>
          <button type="button" className="secondary-btn small" disabled>
            Сохранить черновик
          </button>
        </div>
        <div className="wizard-notice">
          <span>Система автоматически сохраняет черновик каждые 5 минут. Вы можете вернуться к заполнению в любое время.</span>
        </div>

        <div className="wizard-steps">
          {steps.map((s) => (
            <div
              key={s.id}
              className={`wizard-step ${step === s.id ? 'wizard-step--active' : step > s.id ? 'wizard-step--done' : ''}`}
            >
              <span className="wizard-step-number">{s.id}</span>
              <span className="wizard-step-title">{s.title}</span>
            </div>
          ))}
        </div>

        <div className="wizard-body">{renderStepContent()}</div>

        <div className="wizard-actions">
          {step === 1 ? (
            <button type="button" className="secondary-btn" onClick={onBackToCabinet}>
              Назад в личный кабинет
            </button>
          ) : (
            <button type="button" className="secondary-btn" onClick={() => setStep(step - 1)}>
              Назад
            </button>
          )}
          <div className="wizard-actions-right">
            {step < 3 && (
              <button type="button" className="primary-btn" onClick={() => setStep(step + 1)}>
                {step === 1 ? 'Далее: Информация о цифровой инновации' : 'Далее: Характеристики инновации'}
              </button>
            )}
            {step === 3 && (
              <>
                <button type="button" className="secondary-btn" disabled>
                  Сохранить черновик
                </button>
                <button type="button" className="primary-btn" disabled>
                  Отправить заявку
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {renderHelp()}
    </section>
  );
};

export default ApplicationWizard;

