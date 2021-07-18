Feature: Jeopardy
  Scenario: Get a Question
    Given an english speaking user
     When the user says "Give me a jeopardy question"
     Then "jeopardy-skill" should reply with dialog from "jeopardy-question.dialog"

