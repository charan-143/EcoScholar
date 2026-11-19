"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export default function LoginPage() {
  const router=useRouter();
  const [mode,setMode]=useState<"login"|"register">("login");
  const [email,setEmail]=useState(""); const [password,setPassword]=useState("");
  const [displayName,setDisplayName]=useState(""); const [error,setError]=useState(""); const [busy,setBusy]=useState(false);
  async function submit(event:FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError("");
    try {
      const response=await fetch(`${API}/api/auth/${mode}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email,password,...(mode==="register"?{display_name:displayName}:{})})});
      const data=await response.json();
      if(!response.ok) throw new Error(data.detail || "Unable to authenticate");
      localStorage.setItem("ecoscholar_token",data.access_token);
      localStorage.setItem("ecoscholar_user",JSON.stringify(data.user));
      router.push("/");
    } catch(e) { setError(e instanceof Error?e.message:"Unexpected error"); }
    finally { setBusy(false); }
  }
  return <main style={{minHeight:"100vh",display:"grid",placeItems:"center",padding:24,background:"#f4f7f2"}}>
    <section style={{width:"min(100%,440px)",background:"#fff",padding:32,borderRadius:24,boxShadow:"0 18px 60px #183d2414"}}>
      <a href="/" style={{color:"#39734a",fontWeight:700,textDecoration:"none"}}>← EcoScholar</a>
      <p style={{marginTop:30,color:"#5e8066",fontWeight:700,letterSpacing:2,fontSize:12}}>LEARN WITH EVIDENCE</p>
      <h1 style={{fontSize:32,margin:"8px 0"}}>{mode==="login"?"Welcome back":"Create your learner account"}</h1>
      <p style={{color:"#65736a",lineHeight:1.6}}>Save your learning progress and get recommendations based on your interests.</p>
      <form onSubmit={submit} style={{display:"grid",gap:14,marginTop:24}}>
        {mode==="register"&&<label style={{display:"grid",gap:6}}>Name<input required minLength={2} maxLength={120} value={displayName} onChange={e=>setDisplayName(e.target.value)} style={field}/></label>}
        <label style={{display:"grid",gap:6}}>Email<input required type="email" value={email} onChange={e=>setEmail(e.target.value)} style={field}/></label>
        <label style={{display:"grid",gap:6}}>Password<input required minLength={mode==="register"?10:1} type="password" value={password} onChange={e=>setPassword(e.target.value)} style={field}/></label>
        {error&&<p role="alert" style={{color:"#a32d2d",margin:0}}>{error}</p>}
        <button disabled={busy} style={{border:0,borderRadius:12,padding:14,background:"#244f35",color:"white",fontWeight:700,cursor:"pointer"}}>{busy?"Please wait…":mode==="login"?"Sign in":"Create account"}</button>
      </form>
      <button onClick={()=>{setMode(mode==="login"?"register":"login");setError("");}} style={{marginTop:18,border:0,background:"transparent",color:"#39734a",cursor:"pointer"}}>{mode==="login"?"New to EcoScholar? Create an account":"Already registered? Sign in"}</button>
      <p style={{fontSize:12,color:"#829087",marginTop:24}}>New accounts receive the learner role. Educator and admin permissions are assigned by an administrator.</p>
    </section>
  </main>;
}
const field:React.CSSProperties={padding:12,border:"1px solid #d9e2da",borderRadius:10,font:"inherit",background:"#fbfcfa"};
