// Deterministic publication SVGs from archived numeric results. Node >=18, no dependencies.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname,'..');
const data = JSON.parse(fs.readFileSync(path.join(root,'results/strengthening.json'),'utf8'));
const csv = name => fs.readFileSync(path.join(root,'results',name),'utf8').trim().split(/\r?\n/).slice(1).map(s=>s.split(','));
const policy = csv('reference_heldout.csv');
const cal = csv('calibration_sensitivity.csv').map(r=>r.map(Number));
const out = process.argv[2] || path.join(root,'results/figures');
fs.mkdirSync(out,{recursive:true});
const ink='#202832', blue='#0072B2', orange='#D55E00', gray='#677582', teal='#009E73', grid='#D9DEE3';
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const n=x=>Number(x.toFixed(4));
let a=[];
const add=s=>a.push(s);
const text=(x,y,s,opts='')=>add('<text x="'+n(x)+'" y="'+n(y)+'" '+opts+'>'+esc(s)+'</text>');
const line=(x,y,X,Y,opts='')=>add('<line x1="'+n(x)+'" y1="'+n(y)+'" x2="'+n(X)+'" y2="'+n(Y)+'" stroke="'+ink+'" '+opts+'/>');
const rect=(x,y,w,h,c,opts='')=>add('<rect x="'+n(x)+'" y="'+n(y)+'" width="'+n(w)+'" height="'+n(h)+'" fill="'+c+'" '+opts+'/>');
const dot=(x,y,c,r=5,opts='')=>add('<circle cx="'+n(x)+'" cy="'+n(y)+'" r="'+r+'" fill="'+c+'" '+opts+'/>');
const label=(x,y,s)=>text(x,y,s,'font-weight="700" font-size="16"');
const centered='text-anchor="middle"';
const end='text-anchor="end"';
const axisY=(x,y,s)=>text(x,y,s,'transform="rotate(-90 '+x+' '+y+')" '+centered);
function begin(w,h,title,desc){a=[];add('<svg xmlns="http://www.w3.org/2000/svg" width="'+(w/100)+'in" height="'+(h/100)+'in" viewBox="0 0 '+w+' '+h+'" role="img"><title>'+esc(title)+'</title><desc>'+esc(desc)+'</desc><rect width="100%" height="100%" fill="white"/><g font-family="Arial, Liberation Sans, sans-serif" font-size="12" fill="'+ink+'">');}
function save(name){add('</g></svg>');fs.writeFileSync(path.join(out,name+'.svg'),a.join('\n')+'\n');}
function ygrid(x0,x1,ys,vals,fmt=String){for(const v of vals){line(x0,ys(v),x1,ys(v),'stroke-opacity="0.15"');text(x0-8,ys(v)+4,fmt(v),end);}line(x0,ys(vals[0]),x1,ys(vals[0]));line(x0,ys(vals[0]),x0,ys(vals.at(-1)));}
const fmt=v=>String(Number(v.toFixed(3)));
const pct=v=>fmt(v)+'%';
const names=['Independent','Dependent A','Dependent B'], colors=[gray,orange,blue];
const competent=data.counterexample.filter(r=>r.p===.75);
if(competent.length!==3)throw Error('expected three competent distributions');
begin(700,340,'Identical ESS, different majority accuracy','Exact distributions; p=0.75, pairwise correlation zero, ESS=3.');
label(16,24,'(a) Majority correctness');label(350,24,'(b) Distribution of correct votes');
const y=v=>258-v*2.03;
ygrid(50,319,y,[0,25,50,75,100],pct);
axisY(15,154,'Majority correctness (%)');
competent.forEach((r,i)=>{const x=69+i*84,v=r.majority*100;rect(x,y(v),58,258-y(v),colors[i]);text(x+29,y(v)-7,fmt(v)+'%',centered+' font-weight="700"');text(x+29,275,names[i],centered+' font-size="10"');});
line(50,y(75),319,y(75),'stroke-dasharray="4 3"');text(52,299,'Dashed: individual accuracy (75%)','font-size="10"');
const yy=v=>258-v*3.35;const xx=k=>389+k*72;
rect(510,57,160,201,'#E8F3F8');text(590,48,'Majority-correct region',centered+' font-size="10"');
ygrid(384,674,yy,[0,20,40,60],pct);
axisY(350,154,'Probability (%)');
for(let k=0;k<4;k++){competent.forEach((r,i)=>rect(xx(k)+i*19,yy(100*r.q[k]),16,258-yy(100*r.q[k]),colors[i]));text(xx(k)+27,275,k,centered);}
text(529,296,'Number of correct judges (K)',centered);
names.forEach((s,i)=>{rect(384+i*98,313,11,11,colors[i]);text(399+i*98,323,s,'font-size="10"');});
text(50,322,'p = 0.75; pairwise correlation = 0; ESS = 3','font-size="10"');
save('A_ess_counterexample');

begin(700,355,'Synthetic held-out policy comparison','Assumed expenditure and mean error are visualized; feasibility uses dimension-specific limits. Bootstrap intervals are descriptive.');
label(16,24,'(a) Cost–error comparison');label(370,24,'(b) Paired error differences');
const X=v=>49+(v-.024)/.03*284,Y=v=>278-(v-5)/20*220;
ygrid(49,333,Y,[5,10,15,20,25],pct);axisY(14,165,'Mean dimension error (%)');
for(const v of [.025,.03,.035,.04,.045,.05]){line(X(v),278,X(v),283);text(X(v),296,v.toFixed(3),centered+' font-size="10"');}
text(191,319,'Assumed cost per item (USD)',centered);
line(X(.046),45,X(.046),278,'stroke-dasharray="4 3"');text(X(.046)-4,41,'Budget $0.046',end+' font-size="10"');
const labels={'single+single':['Separate',-7,-11,'end'],'panel+panel':['Uniform / weighted',7,-9,'start'],'verifier+verifier':['Verifier only',-6,-10,'end'],'selective+selective':['Selective',8,14,'start'],'shared+shared':['Shared (selected)',7,17,'start']};
for(const r of policy){if(r[0]==='weighted+weighted')continue;const x=X(+r[1]),y=Y(50*(+r[5]+ +r[6])),f=r[8]==='true',l=labels[r[0]];if(f)dot(x,y,blue,r[0]==='shared+shared'?6:4.5);else rect(x-4,y-4,8,8,orange);text(x+l[1],y+l[2],l[0],'font-size="10" text-anchor="'+l[3]+'"');}
dot(54,340,blue,4);text(64,344,'Feasible','font-size="10"');rect(130,336,8,8,orange);text(144,344,'Infeasible','font-size="10"');
const bx=v=>390+(v+6)/10*280;
line(bx(0),52,bx(0),273,'stroke-dasharray="4 3"');
data.bootstrap.forEach((r,i)=>{const y=110+i*100,l=bx(r.lower*100),h=bx(r.upper*100),m=bx(r.mean*100);text(390,y-25,'Dimension '+(i+1),'font-weight="700"');line(l,y,h,y,'stroke-width="2"');line(l,y-5,l,y+5);line(h,y-5,h,y+5);dot(m,y,i===0?orange:blue,5);text(m,y+22,fmt(r.mean*100)+' pp',centered+' font-size="11"');});
line(390,278,670,278);for(const v of [-6,-4,-2,0,2,4]){line(bx(v),278,bx(v),283);text(bx(v),296,v,centered);}
text(530,319,'Shared − separate error (percentage points)',centered+' font-size="11"');text(530,344,'95% paired percentile intervals',centered+' font-size="10"');
save('B_policy_tradeoffs');

begin(700,320,'Conditional error dependence','Reference-defined error correlation before and after one-vote-margin routing.');
const corrColor=v=>{const t=Math.abs(v);const base=v<0?[213,94,0]:[0,114,178];return '#'+base.map(k=>Math.round(255+(k-255)*t).toString(16).padStart(2,'0')).join('');};
['full','routed'].forEach((k,j)=>{const r=data.routing[k],x=85+j*340;label(x-32,24,j?'(b) Routed subset':'(a) Full workload');text(x+90,46,'n = '+r.n,centered);
for(let i=0;i<3;i++){text(x-9,91+i*60,'J'+(i+1),end);text(x+30+i*60,253,'J'+(i+1),centered);for(let h=0;h<3;h++){const v=r.correlation[i][h];rect(x+h*60,55+i*60,59,59,corrColor(v));text(x+30+h*60,91+i*60,v.toFixed(3),centered+(Math.abs(v)>.75?' fill="white"':''));}}
const m=(r.correlation[0][1]+r.correlation[0][2]+r.correlation[1][2])/3;text(x+90,276,'Mean off-diagonal: '+m.toFixed(3),centered+' font-weight="700"');});
for(let i=0;i<101;i++)rect(225+i*2.5,292,2.6,10,corrColor(-1+2*i/100));
text(220,313,'−1',end);text(350,313,'0',centered);text(480,313,'+1');save('C_conditional_dependence');

begin(700,340,'Calibration sensitivity','Mean held-out ESS and one standard deviation among successful fits; fitting failures shown separately.');
label(16,24,'(a) Held-out ESS');label(370,24,'(b) Fitting outcomes');
const cy=v=>270-(v-1.78)/.12*220;
ygrid(55,330,cy,[1.78,1.82,1.86,1.90],v=>v.toFixed(2));axisY(16,165,'Effective sample size');
cal.forEach((r,i)=>{const x=81+i*73,m=r[3],s=r[4];line(x,cy(m-s),x,cy(m+s),'stroke-width="2"');line(x-5,cy(m-s),x+5,cy(m-s));line(x-5,cy(m+s),x+5,cy(m+s));dot(x,cy(m),blue);text(x,288,r[0],centered);});
text(192,315,'Calibration items (categories)',centered);
const sy=v=>270-v*4.4;ygrid(400,675,sy,[0,10,20,30,40,50]);axisY(369,165,'Fitting attempts');
cal.forEach((r,i)=>{const x=420+i*65;rect(x,sy(r[1]),38,270-sy(r[1]),blue);rect(x,sy(r[1]+r[2]),38,sy(r[1])-sy(r[1]+r[2]),orange);text(x+19,288,r[0],centered);});
rect(420,309,10,10,blue);text(435,319,'Successful');rect(530,309,10,10,orange);text(545,319,'Failed');save('D_calibration_sensitivity');

begin(700,300,'Covariance-aware weighting','Analytical independent Bernoulli error indicators with unequal marginal variances.');
label(16,24,'(a) Weighted-mean variance');label(370,24,'(b) Nonnegative optimal weights');
const vy=v=>243-v/.07*195;ygrid(55,330,vy,[0,.02,.04,.06],v=>v.toFixed(2));
axisY(16,150,'Variance');
[data.covariance.uniform_variance,data.covariance.variance].forEach((v,i)=>{const x=95+i*120;rect(x,vy(v),80,243-vy(v),i?blue:gray);text(x+40,vy(v)-8,v.toFixed(6),centered);text(x+40,263,i?'Optimized':'Uniform',centered);});
const wy=v=>243-v/.6*195;ygrid(400,675,wy,[0,.2,.4,.6],v=>pct(v*100));
axisY(369,150,'Weight (%)');
data.covariance.weights.forEach((v,i)=>{const x=420+i*85;rect(x,wy(v),55,243-wy(v),blue);text(x+27.5,wy(v)-8,(v*100).toFixed(2)+'%',centered);text(x+27.5,263,'J'+(i+1),centered);});
text(192,286,'Variance reduction only',centered+' font-size="10"');text(538,286,'Error probabilities: 0.10, 0.30, 0.50',centered+' font-size="10"');save('E_covariance_weighting');
