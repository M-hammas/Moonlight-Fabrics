export const CATEGORIES = [
  { key:"women-clothing", label:"Women Clothing" },
  { key:"women-fragrance", label:"Women Fragrance" },
  { key:"shoes", label:"Shoes" },
  { key:"undergarments", label:"Undergarments" },
];
export const ORDER_STATUSES=["pending","confirmed","processing","shipped","delivered","cancelled"];
export const formatPKR = value => `PKR ${Number(value||0).toLocaleString("en-PK")}`;
