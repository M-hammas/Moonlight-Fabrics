export const cn=(...values)=>values.filter(Boolean).join(" ");
export const slugify=value=>String(value||"").toLowerCase().trim().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
export const getProductPrice=p=>Number(p?.sale_price ?? p?.salePrice ?? p?.price ?? 0);
export const getImage=p=>p?.image || p?.images?.[0] || "";
export const safeJSON=(value,fallback)=>{try{return JSON.parse(value)}catch{return fallback}};
