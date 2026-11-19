'use client';
import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
type Course = { slug:string; title:string; category:string; level:string; duration:string; description:string };
type Source = { id:string; title:string; excerpt:string; source:string; relevance:number; url?:string };
type Recommendation = { course_slug:string; reason:string; score:number };
type Dataset = {id:string;name:string;unit:string;provider:string;source_url:string;download_url:string};

export default function Home() {
  const [courses,setCourses] = useState<Course[]>([]);
  const [question,setQuestion] = useState('How can cities reduce climate emissions?');
  const [answer,setAnswer] = useState('');
  const [sources,setSources] = useState<Source[]>([]);
  const [loading,setLoading] = useState(false);
  const [apiState,setApiState] = useState('Connecting to API');
  const [user,setUser] = useState<{display_name:string;role?:string}|null>(null);
  const [recommendations,setRecommendations] = useState<Recommendation[]>([]);
  const [datasets,setDatasets] = useState<Dataset[]>([]);
  useEffect(() => {
    fetch(`${API}/api/datasets`).then(r=>r.ok?r.json():null).then(d=>{if(d?.datasets)setDatasets(d.datasets)}).catch(()=>{});
    fetch(`${API}/api/courses`).then(r => { if(!r.ok) throw new Error('API unavailable'); return r.json(); })
      .then(d => { setCourses(d); setApiState('API connected'); }).catch(() => setApiState('API unavailable — start Docker Compose'));
    const token=localStorage.getItem('ecoscholar_token');
    const stored=localStorage.getItem('ecoscholar_user');
    if(token && stored) {
      try { setUser(JSON.parse(stored)); } catch { localStorage.removeItem('ecoscholar_user'); }
      fetch(`${API}/api/recommendations/me?interests=climate,biodiversity,energy`,{headers:{Authorization:`Bearer ${token}`}})
        .then(r=>r.ok?r.json():null).then(d=>{if(d?.results)setRecommendations(d.results)}).catch(()=>{});
    }
  },[]);
  async function ask() {
    if(question.trim().length < 3) return;
    setLoading(true); setAnswer(''); setSources([]);
    try {
      const r = await fetch(`${API}/api/assistant/ask`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question})});
      if(!r.ok) throw new Error('Request failed');
      const d = await r.json(); setAnswer(d.answer); setSources(d.sources || []);
    } catch { setAnswer('Could not reach the API. Start the backend and try again.'); }
    finally { setLoading(false); }
  }
  return <main className="shell">
    <header className="top"><a className="brand" href="/">🌱 eco<span>scholar</span></a><nav className="nav"><a href="#learning">Learning paths</a><a href="#assistant">AI assistant</a><a href="#about">About</a></nav><span className="pill">{apiState}</span>{user?.role==="admin"&&<a href="/admin">Admin</a>}{user?<span className="pill">Hi, {user.display_name} <button onClick={()=>{localStorage.removeItem('ecoscholar_token');localStorage.removeItem('ecoscholar_user');setUser(null);setRecommendations([])}}>Sign out</button></span>:<a className="primary" href="/login">Sign in / Join</a>}</header>
    <section className="hero"><div className="hero-copy"><div className="eyebrow">Knowledge for a changing planet</div><h1>Learn deeply.<br/>Live lightly.</h1><p>Build the knowledge to understand environmental challenges and make better-informed decisions. Explore practical lessons, ask evidence-led questions and track your learning journey.</p><a className="primary" href="#learning">Explore learning paths ↗</a></div><div className="visual"><div className="visual-label">A more informed relationship<br/>with our living planet.</div></div></section>
    <section className="stats"><div className="stat"><b>{courses.length || '—'}</b><small>Starter learning modules</small></div><div className="stat"><b>5</b><small>Environmental knowledge themes</small></div><div className="stat"><b>TF-IDF</b><small>Retrieval baseline</small></div></section>
    <section id="datasets"><div className="section-head"><div><div className="eyebrow">Explore real-world indicators</div><h2>Environmental data library</h2></div><span className="muted">{datasets.length} linked datasets</span></div><div className="courses">{datasets.map(d=><article className="course" key={d.id}><div className="course-top"><span>{d.provider}</span><span>{d.unit}</span></div><h3>{d.name}</h3><div className="course-bottom"><a href={d.source_url} target="_blank" rel="noreferrer">View source ↗</a><a href={d.download_url} target="_blank" rel="noreferrer">Download data ↗</a></div></article>)}</div></section>
    <section id="learning"><div className="section-head"><div><div className="eyebrow">Start with the fundamentals</div><h2>Learning paths</h2></div><span className="muted">Curated starter curriculum</span></div><div className="courses">{courses.map(c=><article className="course" key={c.slug}><div className="course-top"><span>{c.category.toUpperCase()}</span><span>{c.duration}</span></div><h3>{c.title}</h3><p>{c.description}</p><div className="course-bottom"><small className="muted">{c.level}</small><a href={`/course/${c.slug}`}>Open module ↗</a></div></article>)}</div></section>
    {recommendations.length>0&&<section><div className="section-head"><div><div className="eyebrow">Your learning signals</div><h2>Recommended next</h2></div></div><div className="courses">{recommendations.map(r=>{const c=courses.find(x=>x.slug===r.course_slug);return c?<article className="course" key={r.course_slug}><div className="course-top"><span>PERSONALIZED</span><span>{Math.round(r.score*100)} match</span></div><h3>{c.title}</h3><p>{r.reason}</p><div className="course-bottom"><a href={`/course/${c.slug}`}>Continue learning ↗</a></div></article>:null})}</div></section>}
    <section id="assistant"><div className="section-head"><div><div className="eyebrow">Explore and reflect</div><h2>Environmental intelligence</h2></div></div><div className="panel"><h3>Ask the EcoScholar assistant</h3><p className="muted">Search the starter knowledge base. Results expose retrieved passages and source notes rather than inventing unsupported answers.</p><div className="field"><input value={question} onChange={e=>setQuestion(e.target.value)} onKeyDown={e=>e.key==='Enter'&&ask()} aria-label="Ask a sustainability question"/><button onClick={ask} disabled={loading}>{loading?'Searching…':'Ask'}</button></div>{answer&&<div className="answer">{answer}{sources.map(s=><div className="source" key={s.id}><b>{s.title}</b><p>{s.excerpt}</p><small>{s.source} · relevance {s.relevance}</small></div>)}</div>}</div></section>
    <section id="about" className="about"><div className="eyebrow">Prototype principles</div><h2>Measure carefully. Communicate honestly.</h2><p className="muted">EcoScholar is an educational prototype. Its starter knowledge base and illustrative footprint factors require authoritative source review before real-world use.</p></section>
    <footer className="foot">EcoScholar · Built with Next.js, FastAPI, PostgreSQL and scikit-learn.</footer>
  </main>;
}
