"use client";
import {useEffect,useState} from "react";
import {useRouter} from "next/navigation";
const API=process.env.NEXT_PUBLIC_API_URL||"http://localhost:8000";
type Account={id:number;email:string;display_name:string;role:"learner"|"educator"|"admin"};
export default function AdminPage(){
 const router=useRouter(); const [users,setUsers]=useState<Account[]>([]); const [error,setError]=useState(""); const [loading,setLoading]=useState(true); const [saving,setSaving]=useState<number|null>(null);
 async function load(){
  const token=localStorage.getItem("ecoscholar_token");
  if(!token){router.push("/login");return;}
  try{const r=await fetch(API+"/api/auth/users",{headers:{Authorization:"Bearer "+token}});if(!r.ok)throw new Error(r.status===403?"Administrator access is required.":"Unable to load accounts.");setUsers(await r.json());}
  catch(e){setError(e instanceof Error?e.message:"Request failed");}finally{setLoading(false);}
 }
 useEffect(()=>{load();},[]);
 async function updateRole(userId:number,role:Account["role"]){
  const token=localStorage.getItem("ecoscholar_token");setSaving(userId);setError("");
  try{const r=await fetch(API+"/api/auth/users/"+userId+"/role",{method:"PATCH",headers:{"Content-Type":"application/json",Authorization:"Bearer "+token},body:JSON.stringify({role})});const d=await r.json();if(!r.ok)throw new Error(d.detail||"Role update failed");setUsers(current=>current.map(u=>u.id===userId?d:u));}
  catch(e){setError(e instanceof Error?e.message:"Role update failed");}finally{setSaving(null);}
 }
 return <main className="shell"><a href="/">← EcoScholar</a><div className="eyebrow">ADMINISTRATION</div><h1>Account management</h1><p className="muted">Assign learner, educator and administrator roles. Only administrators can access this page.</p>{loading?<p>Loading accounts…</p>:<section className="panel"><h2>{users.length} accounts</h2>{users.map(u=><div key={u.id} style={{display:"flex",justifyContent:"space-between",gap:16,alignItems:"center",padding:"14px 0",borderBottom:"1px solid #e5ebe5"}}><div><b>{u.display_name}</b><div className="muted">{u.email}</div></div><select aria-label={"Role for "+u.email} value={u.role} disabled={saving===u.id} onChange={e=>updateRole(u.id,e.target.value as Account["role"])}><option value="learner">Learner</option><option value="educator">Educator</option><option value="admin">Admin</option></select></div>)}</section>}{error&&<p role="alert" style={{color:"#a32d2d"}}>{error}</p>}</main>;
}
