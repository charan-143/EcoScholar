'use client';
import {useEffect,useState} from 'react';
import {useParams} from 'next/navigation';

const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000';
type Course={title:string;category:string;level:string;duration:string;description:string;content:string;slug:string};
type Quiz={course_slug:string;questions:{question:string;options:string[]}[]};

export default function CoursePage(){
 const params=useParams<{slug:string}>();
 const [course,setCourse]=useState<Course|null>(null);
 const [quiz,setQuiz]=useState<Quiz|null>(null);
 const [answers,setAnswers]=useState<number[]>([]);
 const [result,setResult]=useState<any>(null);
 const [error,setError]=useState('');
 const [loading,setLoading]=useState(true);
 useEffect(()=>{
  let active=true;
  Promise.all([
   fetch(`${API}/api/courses`).then(r=>{if(!r.ok)throw new Error('Unable to load course catalogue');return r.json()}),
   fetch(`${API}/api/quizzes/${params.slug}`).then(r=>r.ok?r.json():null)
  ]).then(([all,q])=>{
   if(!active)return;
   const found=(all as Course[]).find(c=>c.slug===params.slug)||null;
   setCourse(found);setQuiz(q);if(!found)setError('This learning module could not be found.');
  }).catch(()=>{if(active)setError('Could not connect to EcoScholar. Check that the API is running.');})
  .finally(()=>{if(active)setLoading(false)});
  return ()=>{active=false};
 },[params.slug]);
 async function submit(){
  setError('');
  try{
   const response=await fetch(`${API}/api/quizzes/submit`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({course_slug:params.slug,answers})});
   const data=await response.json();
   if(!response.ok)throw new Error(data.detail||'Quiz submission failed');
   setResult(data);
  }catch(e){setError(e instanceof Error?e.message:'Quiz submission failed');}
 }
 const complete=!!quiz&&quiz.questions.every((_,i)=>Number.isInteger(answers[i]));
 if(loading)return <main className="shell">Loading module…</main>;
 if(!course)return <main className="shell"><a href="/">← EcoScholar</a><h1>Module unavailable</h1><p>{error}</p></main>;
 return <main className="shell">
  <a href="/">← EcoScholar</a>
  <p>{course.category} · {course.level} · {course.duration}</p>
  <h1>{course.title}</h1><p>{course.description}</p>
  <section className="panel"><h2>Lesson</h2><p style={{lineHeight:1.8}}>{course.content}</p></section>
  {quiz&&<section className="panel"><h2>Knowledge check</h2>
   {quiz.questions.map((q,i)=><div key={i} style={{margin:'22px 0'}}><b>{i+1}. {q.question}</b>{q.options.map((o,j)=><label key={j} style={{display:'block',padding:8}}><input type="radio" name={`q${i}`} checked={answers[i]===j} onChange={()=>{setAnswers(a=>{const n=[...a];n[i]=j;return n});setResult(null)}}/> {o}</label>)}</div>)}
   <button onClick={submit} disabled={!complete}>Submit answers</button>
   {result&&<p><b>Your score: {result.score}/{result.total} ({result.percentage}%)</b><br/>{result.message}</p>}
  </section>}
  {error&&<p role="alert">{error}</p>}
 </main>;
}
