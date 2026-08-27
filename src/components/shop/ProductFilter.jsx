import React from "react";
import {CATEGORIES} from "../../utils/constants";
export default function ProductFilter({category,setCategory,sort,setSort,sale,setSale}){
 return <div className="filters">
   <select value={category||""} onChange={e=>setCategory(e.target.value)}><option value="">All categories</option>{CATEGORIES.map(c=><option value={c.key} key={c.key}>{c.label}</option>)}</select>
   <select value={sort} onChange={e=>setSort(e.target.value)}><option value="featured">Featured</option><option value="price-low">Price: low to high</option><option value="price-high">Price: high to low</option><option value="rating">Top rated</option></select>
   <label className="filter-check"><input type="checkbox" checked={sale} onChange={e=>setSale(e.target.checked)}/> Sale only</label>
 </div>
}
