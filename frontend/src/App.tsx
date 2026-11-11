import { useEffect, useMemo, useRef, useState } from 'react';
import { UploadCloud, Ruler, Layers3, ScanLine, Info, ShieldCheck, RotateCcw, FileImage } from 'lucide-react';

type ImageInfo = {type:'png'|'svg'; width:number; height:number; units:string; colors:{hex:string;pixels:number}[]; preview_svg?:string};
type Matrix = {width_mm:number; height_mm:number; margin_mm:number};
const DEFAULT:Matrix = {width_mm:350,height_mm:275,margin_mm:5};
const n=(value:number)=>Number.isFinite(value)?value.toFixed(1):'—';

export default function App(){
  const [matrix,setMatrix]=useState<Matrix>(DEFAULT);
  const [info,setInfo]=useState<ImageInfo|null>(null);
  const [url,setUrl]=useState<string|null>(null);
  const [name,setName]=useState<string>('');
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(false);
  const [rotation,setRotation]=useState(0);
  const fileRef=useRef<HTMLInputElement>(null);
  useEffect(()=>()=>{if(url) URL.revokeObjectURL(url)},[url]);
  const width=Math.max(0,matrix.width_mm),height=Math.max(0,matrix.height_mm),margin=Math.max(0,matrix.margin_mm);
  const usableW=Math.max(0,width-2*margin), usableH=Math.max(0,height-2*margin);
  const valid = width>0&&height>0&&width<=350&&height<=275&&usableW>0&&usableH>0;
  const fit=useMemo(()=>{
    if(!info||!valid)return null;
    const sw=rotation%180===0?info.width:info.height, sh=rotation%180===0?info.height:info.width;
    const scale=Math.min(usableW/sw,usableH/sh);const w=scale*sw,h=scale*sh;
    return {w,h,x:margin+(usableW-w)/2,y:margin+(usableH-h)/2};
  },[info,valid,rotation,usableW,usableH,margin]);
  async function readFile(file:File){
    setLoading(true);setError('');setInfo(null);setUrl(null);setRotation(0);
    try{
      if(!/\.(png|svg)$/i.test(file.name))throw new Error('Formato não suportado: use .png ou .svg');
      const form=new FormData();form.append('file',file);
      const response=await fetch('/api/import/inspect',{method:'POST',body:form});
      const payload=await response.json();
      if(!response.ok)throw new Error(typeof payload.detail==='string'?payload.detail:'Falha ao importar imagem');
      setInfo(payload as ImageInfo);setName(file.name);
      // SVG is rendered only as an image, never inserted as HTML or inline DOM.
      setUrl(URL.createObjectURL(file));
    }catch(e){setError(e instanceof Error?e.message:'Erro desconhecido');}
    finally{setLoading(false)}
  }
  function changeDimension(key:keyof Matrix,value:string){setMatrix(x=>({...x,[key]:Number(value)}));}
  const preset=(key:string)=>{if(key==='A4')setMatrix({width_mm:297,height_mm:210,margin_mm:5});if(key==='B5')setMatrix({width_mm:250,height_mm:176,margin_mm:5});if(key==='Custom')setMatrix(DEFAULT)};
  return <div className="app">
    <aside className="sidebar">
      <header className="brand"><div className="brand-icon"><ScanLine size={24}/></div><div><strong>LaserCraft <span>Studio</span></strong><small>LASER DESIGN WORKSPACE</small></div></header>
      <div className="section-heading"><UploadCloud size={17}/> ARQUIVO DE ENTRADA</div>
      <input ref={fileRef} type="file" accept=".svg,.png,image/svg+xml,image/png" hidden onChange={e=>{const f=e.target.files?.[0];if(f)void readFile(f);e.target.value='';}}/>
      <button className="upload" onClick={()=>fileRef.current?.click()} disabled={loading}><UploadCloud size={27}/><strong>{loading?'Processando arquivo...':'Importar SVG ou PNG'}</strong><span>Escolha um arquivo do computador</span><small>Limite de 10 MB</small></button>
      {error&&<div className="alert">{error}</div>}
      {info&&<div className="file-pill"><FileImage size={19}/><div><strong title={name}>{name}</strong><small>{n(info.width)} × {n(info.height)} {info.units}</small></div></div>}
      <div className="section-heading"><Ruler size={17}/> MATRIZ DE TRABALHO</div>
      <label className="label">Formatos de referência</label><div className="presets"><button onClick={()=>preset('A4')}>A4 (paisagem)</button><button onClick={()=>preset('B5')}>B5 (paisagem)</button><button onClick={()=>preset('Custom')}>350 × 275</button></div>
      <div className="fields"><label>Largura (mm)<input type="number" min="1" max="350" value={matrix.width_mm} onChange={e=>changeDimension('width_mm',e.target.value)}/></label><label>Altura (mm)<input type="number" min="1" max="275" value={matrix.height_mm} onChange={e=>changeDimension('height_mm',e.target.value)}/></label></div>
      <label className="label">Margem de segurança (mm)<input type="number" min="0" max="50" value={matrix.margin_mm} onChange={e=>changeDimension('margin_mm',e.target.value)}/></label>
      {!valid&&<div className="alert">Dimensões inválidas: limite 350 × 275 mm e margem menor que metade de cada dimensão.</div>}
      <div className="area-metric"><span>Área útil</span><strong>{n(usableW)} × {n(usableH)} mm</strong></div>
      <div className="section-heading"><Layers3 size={17}/> PROCESSAMENTO</div>
      <div className="future"><span>Separação de cores</span><small>Sprint 2</small></div><div className="future"><span>Contornos e trajetórias</span><small>Sprint 2–3</small></div><div className="future"><span>Exportação e projetos</span><small>Sprint 4</small></div>
    </aside>
    <main className="workspace">
      <div className="topbar"><div><strong>Preparação de projeto</strong><span className="separator">/</span><span>Sprint 0</span></div><div className="status"><ShieldCheck size={16}/> Visualização geométrica</div></div>
      <div className="toolbar"><span>Área física em milímetros</span><button onClick={()=>setRotation(x=>(x+90)%360)} disabled={!info}>Girar imagem 90°</button><button onClick={()=>{setMatrix(DEFAULT);setRotation(0)}}><RotateCcw size={15}/> Redefinir</button></div>
      <div className="canvas-container"><div className="canvas-shell" style={{aspectRatio:`${Math.max(width,1)}/${Math.max(height,1)}`}}>
        <div className="safe-area" style={{left:`${100*margin/Math.max(width,1)}%`,top:`${100*margin/Math.max(height,1)}%`,width:`${100*usableW/Math.max(width,1)}%`,height:`${100*usableH/Math.max(height,1)}%`}}/>
        {url&&fit&&<div className="placed" style={{left:`${100*fit.x/width}%`,top:`${100*fit.y/height}%`,width:`${100*fit.w/width}%`,height:`${100*fit.h/height}%`}}><img src={url} alt="Imagem importada" style={{transform:`rotate(${rotation}deg)`,width:rotation%180===0?'100%':`${100*fit.h/fit.w}%`,height:rotation%180===0?'100%':`${100*fit.w/fit.h}%`}}/></div>}
        {!info&&<div className="placeholder"><div className="placeholder-icon"><UploadCloud size={40}/></div><strong>Sua área de criação</strong><span>Importe um arquivo para visualizar o enquadramento</span><button onClick={()=>fileRef.current?.click()}>Selecionar imagem</button></div>}
        <span className="origin">0,0</span>
      </div><div className="measure">{n(width)} mm × {n(height)} mm</div></div>
      <div className="bottom-panel"><div className="panel-header"><Info size={17}/><strong>Propriedades da projeção</strong></div><div className="stats"><div><small>Área útil</small><strong>{n(usableW)} × {n(usableH)} mm</strong></div><div><small>Imagem projetada</small><strong>{fit?`${n(fit.w)} × ${n(fit.h)} mm`:'—'}</strong></div><div><small>Origem X / Y</small><strong>{fit?`${n(fit.x)} / ${n(fit.y)} mm`:'—'}</strong></div><div><small>Rotação</small><strong>{rotation}°</strong></div></div>
      {info&&info.type==='png'&&<div className="colors"><small>Cores predominantes aproximadas (não são camadas de corte):</small><div className="swatches">{info.colors.map((c,i)=><span key={i} title={`${c.hex}: ${c.pixels} pixels amostrados`} style={{backgroundColor:c.hex}}/>)}</div></div>}
      <div className="notice">Sprint 0: esta prévia confirma proporção e posição na matriz. Não representa energia, largura real do feixe ou execução física de corte.</div></div>
    </main>
  </div>;
}
