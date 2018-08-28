using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class gcc : MonoBehaviour {
    public Text timer;
    public Text finalText;
    public GameObject egCard;
    public Button bb;

    string scoreTracker = "";
    string timerTracker = "00000000000000000000";
    string secret = "d464a7a0-8118-11e8-adc0-fa7ae01bbebc";
    string st = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    void randomSpot() {
        Vector3 position = new Vector3(
        Random.Range(0, Screen.width),
        Random.Range(0, Screen.height), 0);

        Vector3 kk = Camera.main.ScreenToWorldPoint(position);
        kk.z = 0f;

        this.transform.position = kk;

        Button btn = bb.GetComponent<Button>();
        btn.onClick.AddListener(bbC);
    }

    void bbC() {
        SceneManager.LoadScene("Menu");
    }

    int getScore() {
        int l = scoreTracker.Length;
        return l / 7;
    }

    void setScore(int s) {
        scoreTracker = "";
        for (int i = 0; i < s * 7; i++) {
            scoreTracker += st[Random.Range(0, st.Length - 1)];
        }
    }

    int getTimer() {
        return timerTracker.Length;
    }

    void setTimer(int t) {
        timerTracker = "";
        for (int i = 0; i < t; i++) {
            timerTracker += st[Random.Range(0, st.Length - 1)];
        }
    }

    bool endgame = false;

    void tt() {
        setTimer(getTimer() - 1);
        timer.text = string.Format("Timer: {0} s", getTimer());

        if (getTimer() <= 0) {
            StartCoroutine(EndGame());
        }
    }

    IEnumerator EndGame() {
        CancelInvoke("tt");
        endgame = true;
        this.GetComponent<SpriteRenderer>().color = new Color(0f, 0f, 0f, 0f);

        string username = "revalo";
        string ep = "http://localhost:5000/";
        int score = getScore();

        if (System.IO.File.Exists("username.txt")) {
            username = System.IO.File.ReadAllText("username.txt").Trim();
        }

        if (System.IO.File.Exists("ep.txt")) {
            ep = System.IO.File.ReadAllText("ep.txt").Trim();
        }

        ep = ep + username + "/verify";

        WWWForm form = new WWWForm();
        form.AddField("jwt", GetJWT(username, score));

        UnityWebRequest uwr = UnityWebRequest.Post(ep, form);
        yield return uwr.SendWebRequest();

        egCard.SetActive(true);
        finalText.text = string.Format("Number unlocked: {0}\n{1}", getScore(), uwr.downloadHandler.text);
    }

    string GetJWT(string username, int score) {
        string payload = "{\"username\": \"" + username + "\", \"score\": " + score.ToString() +"}";
        string token = JWT.JsonWebToken.Encode(payload, secret, JWT.JwtHashAlgorithm.HS256);

        return token;
    }

	// Use this for initialization
	void Start () {
        randomSpot();

        InvokeRepeating("tt", 1.0f, 1.0f);
    }

    void OnMouseDown() {
        if (endgame) return;

        setScore(getScore() + 1);
        randomSpot();
    }

    // Update is called once per frame
    void Update () {
        
    }
}
