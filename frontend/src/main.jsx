import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ArrowRight, Check, Droplets, MapPin, Recycle, Route, Search, Send, ShieldCheck, Sparkles, Zap } from 'lucide-react';
import './styles.css';

const examples = [
  { label: 'Water supply', icon: Droplets, text: 'There has been no water supply in our locality for the past four days.' },
  { label: 'Waste collection', icon: Recycle, text: 'Garbage has not been collected from our street for over a week.' },
  { label: 'Road damage', icon: Route, text: 'The main road in our area has several large potholes causing accidents.' },
];

function App() {
  const [text, setText] = useState('');
  const [category, setCategory] = useState('');
  const [wasTranslated, setWasTranslated] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const chooseExample = (example) => {
    setText(example.text);
    setCategory('');
    setWasTranslated(false);
    setError('');
  };

  async function classify(event) {
    event.preventDefault();
    const grievance = text.trim();
    if (!grievance) return;
    setLoading(true);
    setCategory('');
    setWasTranslated(false);
    setError('');
    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: grievance }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'We could not classify this report. Please try again.');
      setCategory(data.category);
      setWasTranslated(Boolean(data.translated));
    } catch (requestError) {
      setError(requestError.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Nagrik home">
          <span className="brand-icon">न</span><span>Nagrik</span>
        </a>
        <div className="service-tag"><span className="status-dot" /> Civic support desk</div>
      </header>

      <main id="top">
        <section className="hero">
          <div className="eyebrow"><Sparkles size={14} /> YOUR VOICE, ROUTED TO THE RIGHT TEAM</div>
          <h1>Make your community<br className="desktop-break" /> better, one report at a time.</h1>
          <p>Describe the civic issue you’re facing. We’ll identify the right department so your concern can reach the people who can help.</p>
        </section>

        <div className="content-grid">
          <section className="card form-card">
            <div className="card-heading">
              <div><div className="section-icon"><Send size={17} /></div></div>
              <div><h2>Tell us what’s happening</h2><p>Include where it is and how long it has been going on, if you can.</p></div>
            </div>
            <form onSubmit={classify}>
              <label htmlFor="grievance"><span>Your grievance</span><span className="counter">{text.length} <span>/ 1000</span></span></label>
              <textarea id="grievance" maxLength={1000} required value={text} onChange={(event) => { setText(event.target.value); setCategory(''); setError(''); }} placeholder="For example: The streetlights on Park Road have been out for a week, making it difficult to walk safely at night." />
              <div className="examples"><span className="examples-label">TRY AN EXAMPLE</span>{examples.map(({ label, icon: Icon, ...example }) => <button type="button" className="example" key={label} onClick={() => chooseExample(example)}><Icon size={14} /> {label}</button>)}</div>
              {error && <div className="error-message" role="alert">{error}</div>}
              <div className="form-footer">
                <button className="primary-button" type="submit" disabled={loading || !text.trim()}>{loading ? 'Finding a department…' : 'Find the right department'}<ArrowRight size={17} /></button>
                <span className="privacy"><ShieldCheck size={14} /> Common Marathi/Hindi issues are handled locally; other text may be sent to Google Translate.</span>
              </div>
            </form>
            {category && <div className="result" aria-live="polite"><div className="result-icon"><Check size={18} /></div><div><p className="result-label">SUGGESTED DEPARTMENT</p><h3>{category}</h3><p className="result-note">{wasTranslated ? 'Your complaint was translated to English before classification. ' : ''}Your concern is ready to be directed to the team responsible for this service.</p></div></div>}
          </section>

          <aside className="card aside-card">
            <div className="aside-title"><span className="aside-title-icon"><Zap size={16} /></span><h2>How it works</h2></div>
            <div className="steps">
              <div className="step"><span className="step-number">01</span><div><h3>Describe the issue</h3><p>Tell us what happened and where. A few clear details help.</p></div></div>
              <div className="step"><span className="step-number">02</span><div><h3>We find the right team</h3><p>Your message is matched to the civic service that handles it.</p></div></div>
              <div className="step"><span className="step-number">03</span><div><h3>Get a department</h3><p>See which department should take a look at your concern.</p></div></div>
            </div>
            <div className="languages"><div className="language-heading"><MapPin size={14} /><span>WRITE IN YOUR LANGUAGE</span></div><div className="language-pills"><span>English</span><span>हिन्दी</span><span>मराठी</span></div></div>
            <div className="aside-note"><Search size={16} /><span>Clear details help us route your concern to the right place.</span></div>
          </aside>
        </div>
        <footer><span>न Nagrik Civic Support</span><span>Helping communities get heard</span></footer>
      </main>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);
