export const isEmail=value=>/^\S+@\S+\.\S+$/.test(String(value||""));
export const required=value=>String(value||"").trim().length>0;
export const minLength=(value,n)=>String(value||"").length>=n;
export function validateCheckout(data){
  const errors={};
  if(!required(data.name)) errors.name="Name is required";
  if(!isEmail(data.email)) errors.email="Enter a valid email";
  if(!required(data.phone)) errors.phone="Phone is required";
  if(!required(data.address)) errors.address="Address is required";
  if(!required(data.city)) errors.city="City is required";
  return errors;
}
