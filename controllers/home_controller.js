// import { Request, Response, NextFunction } from "express";

const home = async (req, res) => {
    const session = req.dbSession;
    console.log("home");
    //example for db connection
    session.load('employees/1-A')
        .then(employee => {
            if (employee) {
                res.send(`Employee Last Name: ${employee.LastName}`);
            } else {
                res.status(404).send('Employee not found');
            }
            return session.saveChanges();
        })
};

module.exports = { home };
