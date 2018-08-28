using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class bruh : MonoBehaviour {
    public Button btn;
	// Use this for initialization
	void Start () {
        Button btn1 = btn.GetComponent<Button>();
        btn1.onClick.AddListener(clll);
    }
	
    void clll() {
        SceneManager.LoadScene("Catch");
    }

	// Update is called once per frame
	void Update () {
		
	}
}
