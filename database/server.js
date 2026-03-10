  import express from "express";
  import cors from "cors";

  const app = express();
  app.use(express.json())
  app.use(cors())

  app.get('/getInfo',async (req,res)=>{
    res.json({"message":[12,23,4]})
  })

  app.get('/getAge',async(req,res)=>{
    res.json({"age":21})
  })

  app.post('/fetchFromForm',async(req,res)=>{
    const {username,password} = req.body
    res.json({'username':username,'password':password})
  })

  app.listen(5000, () => {
    console.log("Server running at http://localhost:5000");
  });


