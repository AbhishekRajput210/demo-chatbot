"use client";
import { useState, useEffect, useMemo, useRef, MutableRefObject } from "react";
import Chatscreen from "@/components/Chatscreen";
import DexChatscreen from "./dextrade";
import DocChatscreen from "./documentation";
import { Switch, Route, useHistory, useLocation } from "react-router-dom";
import {
    generateQuestions,
    generateAndRunSQL,
    generatePlotlyFigure,
  } from "@/actions/actions";

interface Type{
anchor: MutableRefObject<null>
}

const STEPS = [
  {
    path: "/",
    component: Chatscreen,
    hideTabs: true,
    requiredProps: [
      "generateQuestions",
      "generateAndRunSQL",
      "generatePlotlyFigure",
    ],
  },
  {
    path: "/dexTrade",
    component: DexChatscreen,
    hideTabs: true,
    requiredProps: [
      "generateQuestions",
      "generateAndRunSQL",
      "generatePlotlyFigure",
    ],
  },
  {
    path: "/documentation",
    component: DocChatscreen,
    hideTabs: true,
    requiredProps: [
      "generateQuestions",
      "generateAndRunSQL",
      "generatePlotlyFigure",
    ],
  },
];

const ChatController = ({ anchor }: Type) => {
  return (
    <>
        <Switch>
          {STEPS.map((step, idx) => (
            <Route key={idx} path={step.path} exact>
              <step.component 
              generateQuestions={generateQuestions}
              generateAndRunSQL={generateAndRunSQL}
              generatePlotlyFigure={generatePlotlyFigure}
              />
            </Route>
          ))}
        </Switch>
        {/* <Chatscreen 
        generateQuestions={generateQuestions}
        generateAndRunSQL={generateAndRunSQL}
        generatePlotlyFigure={generatePlotlyFigure}
        /> */}
    </>
  );
}

export default ChatController;
