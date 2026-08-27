import React from "react";
import ProductCard from "./ProductCard";
import Loader from "../common/Loader";
export default function ProductGrid({products,loading=false}){
 if(loading)return <Loader label="Loading products..."/>;
 if(!products?.length)return <div className="empty-state"><div>◌</div><h3>No products found</h3><p>Try changing your filters or search.</p></div>;
 return <div className="product-grid grid">{products.map((p,i)=><ProductCard key={p.id} product={p} index={i}/>)}</div>
}
