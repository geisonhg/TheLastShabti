using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

/// <summary>
/// Fixes the S1→S2 passage block.
///
/// Root causes:
/// 1. S2_Plat1 was at (18, 2.2, 0) — 1-unit gap + 0.5-unit rise from S1_Landing.
///    Fix: move to (16, 1.7, 0) so it overlaps S1_Landing at the same height.
///
/// 2. S2_WallL, S2_WallR, S2_Floor_Main all start at x=17 with left-facing collision
///    surfaces that appear to the player as a closed "entrance wall" and can catch
///    the player's Rigidbody capsule during the fall off S2_Plat1.
///    Fix: extend all S2 corridor geometry to start at x=15 (where S2_Plat1 starts),
///    so the S2 space opens up smoothly alongside the transition platforms.
///
/// 3. ENV_Archway instances received near-zero BoxColliders from LevelBuilder.
///    Fix: disable them so they are purely visual.
///
/// 4. S3_Ceiling at y=10.5 (bottom 10.25) exactly blocked clearing OBS_FallingBlock.
///    Fix: raise to y=14 (bottom 13.75) so the full jump arc fits.
///
/// 5. OBS_FallingBlock had MovableObs(horizontal X) — never fell, blocked gap between
///    S3_StaticB and S3_Exit at head height.
///    Fix: replace with MovingPlatform(Y) starting at y=10, ±1.5 oscillation.
///
/// Run via  TheLastShabti > Fix S1→S2 Passage
/// </summary>
public static class FixPassage
{
    [MenuItem("TheLastShabti/Fix S1→S2 Passage")]
    public static void Run()
    {
        var scene = EditorSceneManager.OpenScene(
            "Assets/Scenes/LVL_MainPyramid.unity", OpenSceneMode.Single);

        bool changed = false;

        // ── 1. Move S2_Plat1 to overlap S1_Landing at the same height ─────────
        var s2Plat1 = GameObject.Find("S2_Plat1");
        if (s2Plat1 != null)
        {
            s2Plat1.transform.position = new Vector3(16f, 1.7f, 0f);
            EditorUtility.SetDirty(s2Plat1);
            Debug.Log("[FixPassage] S2_Plat1 at (16, 1.7, 0) — overlaps S1_Landing, same height.");
            changed = true;
        }
        else
        {
            Debug.LogWarning("[FixPassage] S2_Plat1 not found — already moved?");
        }

        // ── 2. Extend S2_SafeFloor left to cover the transition zone ──────────
        // Old: center (26, 0.25, 0) scale (14, 0.5, 6) → x=19..33
        // New: center (24, 0.25, 0) scale (18, 0.5, 6) → x=15..33
        var safeFloor = GameObject.Find("S2_SafeFloor");
        if (safeFloor != null)
        {
            safeFloor.transform.position   = new Vector3(24f, 0.25f, 0f);
            safeFloor.transform.localScale = new Vector3(18f, 0.5f, 6f);
            EditorUtility.SetDirty(safeFloor);
            Debug.Log("[FixPassage] S2_SafeFloor extended to x=15..33.");
            changed = true;
        }

        // ── 3. Extend S2_Floor_Main left — removes the blocking left face at x=17
        // Old: center (28, 0.7, 0) scale (22, 0.5, 8) → x=17..39
        // New: center (27, 0.7, 0) scale (24, 0.5, 8) → x=15..39
        var floorMain = GameObject.Find("S2_Floor_Main");
        if (floorMain != null)
        {
            floorMain.transform.position   = new Vector3(27f, 0.7f, 0f);
            floorMain.transform.localScale = new Vector3(24f, 0.5f, 8f);
            EditorUtility.SetDirty(floorMain);
            Debug.Log("[FixPassage] S2_Floor_Main extended to x=15..39 — left face moved from x=17 to x=15.");
            changed = true;
        }

        // ── 4. Extend S2_WallL left — removes the blocking left face at x=17 ──
        // Old: center (28, 4.5, -5) scale (22, 9, 0.5) → x=17..39
        // New: center (27, 4.5, -5) scale (24, 9, 0.5) → x=15..39
        var wallL = GameObject.Find("S2_WallL");
        if (wallL != null)
        {
            wallL.transform.position   = new Vector3(27f, 4.5f, -5f);
            wallL.transform.localScale = new Vector3(24f, 9f, 0.5f);
            EditorUtility.SetDirty(wallL);
            Debug.Log("[FixPassage] S2_WallL extended to x=15..39.");
            changed = true;
        }

        // ── 5. Extend S2_WallR left ───────────────────────────────────────────
        var wallR = GameObject.Find("S2_WallR");
        if (wallR != null)
        {
            wallR.transform.position   = new Vector3(27f, 4.5f, 5f);
            wallR.transform.localScale = new Vector3(24f, 9f, 0.5f);
            EditorUtility.SetDirty(wallR);
            Debug.Log("[FixPassage] S2_WallR extended to x=15..39.");
            changed = true;
        }

        // ── 6. Extend S2_Ceiling left (visual consistency) ────────────────────
        var ceiling = GameObject.Find("S2_Ceiling");
        if (ceiling != null)
        {
            ceiling.transform.position   = new Vector3(27f, 8f, 0f);
            ceiling.transform.localScale = new Vector3(24f, 0.5f, 10f);
            EditorUtility.SetDirty(ceiling);
            Debug.Log("[FixPassage] S2_Ceiling extended to x=15..39.");
            changed = true;
        }

        // ── 7. Disable BoxColliders on all ENV_Archway props (they are purely
        //       visual; LevelBuilder gave them near-zero colliders that can still
        //       interfere with Rigidbody tunnelling at low frame rates) ──────────
        int archwayFixed = 0;
        var allGOs = Object.FindObjectsByType<GameObject>(
            FindObjectsInactive.Include, FindObjectsSortMode.None);
        foreach (var go in allGOs)
        {
            if (go.name != "ENV_Archway") continue;
            var bc = go.GetComponent<BoxCollider>();
            if (bc != null && bc.enabled)
            {
                bc.enabled = false;
                EditorUtility.SetDirty(go);
                archwayFixed++;
            }
        }
        if (archwayFixed > 0)
        {
            Debug.Log($"[FixPassage] Disabled BoxCollider on {archwayFixed} ENV_Archway instance(s).");
            changed = true;
        }

        // ── S3→S4 FIXES ─────────────────────────────────────────────────────────
        //
        // S4_WallBk was placed at x=58 as the west wall of the Shaft of Ra, but
        // S3_Exit ends at x=57.5 and S4_Entry starts at x=57.5 — so the wall's
        // left face at x=57.75 completely blocks the player from entering S4.
        // Fix: move S4_WallBk to x=65 so it becomes the east boundary of the shaft.
        //
        // Additionally S4_Entry top (y=8.15) is 0.5 units higher than S3_Exit top
        // (y=7.65).  A Rigidbody capsule cannot step up 0.5 units automatically.
        // Fix: lower S4_Entry to y=7.5 so its top matches S3_Exit (both at y=7.65).

        // S4_WallBk was the west wall of the shaft at x=58, blocking entry.
        // We move it completely out of the play area (x=80) so it never interferes
        // with entry to S4 OR with the S5_Jump2 platform (x=62.8-65.2) that was
        // previously clipped by the wall when it was at x=65.
        var wallBk = GameObject.Find("S4_WallBk");
        if (wallBk != null)
        {
            wallBk.transform.position = new Vector3(80f, 14f, 0f);
            EditorUtility.SetDirty(wallBk);
            Debug.Log("[FixPassage] S4_WallBk moved to x=80 — shaft entrance and S5 jumps now clear.");
            changed = true;
        }

        var s4Entry = GameObject.Find("S4_Entry");
        if (s4Entry != null)
        {
            s4Entry.transform.position = new Vector3(59f, 7.5f, 0f);
            EditorUtility.SetDirty(s4Entry);
            Debug.Log("[FixPassage] S4_Entry lowered to y=7.5 — top now flush with S3_Exit (y=7.65).");
            changed = true;
        }

        // ── S3_Ceiling: raise from y=10.5 → y=14 ────────────────────────────
        // At y=10.5 the ceiling cap exactly equalled what the player needed to clear
        // OBS_FallingBlock (top 9.25 → needs center 10.25 → hits ceiling at 9.25).
        // At y=14 the ceiling is always above the player's jump peak (12.15 from S3_Exit)
        // and the block can oscillate freely up to y=11.5 without touching the ceiling.
        var s3Ceil = GameObject.Find("S3_Ceiling");
        if (s3Ceil != null)
        {
            s3Ceil.transform.position   = new Vector3(46.5f, 14.0f, 0f);
            s3Ceil.transform.localScale = new Vector3(19f, 0.5f, 10f);
            EditorUtility.SetDirty(s3Ceil);
            Debug.Log("[FixPassage] S3_Ceiling raised to y=14 (bottom 13.75) — full jump clearance in S3.");
            changed = true;
        }

        // ── OBS_FallingBlock: replace OCP MovableObs (horizontal X) with Y-fall ─
        // In the scene the block had MovableObs with horizontal=1 (slides on X).
        // That means it was never falling — it just drifted sideways at head height,
        // blocking the gap between S3_StaticB and S3_Exit.
        // Fix: remove MovableObs, add MovingPlatform Y-axis starting at y=10
        // (bottom 9.75 — clears the player's head when standing on StaticB).
        // It oscillates ±1.5: falls to y=8.5 (bottom 8.25, clips standing player
        // → "get off StaticB!") and rises to y=11.5 (clear).  Ceiling at y=14 gives
        // the block 2.25 units of headroom at the top.
        var fallBlock = GameObject.Find("OBS_FallingBlock");
        if (fallBlock != null)
        {
            var obs = fallBlock.GetComponent<MovableObs>();
            if (obs != null) Object.DestroyImmediate(obs);

            fallBlock.transform.position = new Vector3(52f, 10.0f, 0f);
            EditorUtility.SetDirty(fallBlock);

            var mp = fallBlock.AddComponent<MovingPlatform>();
            var smp = new SerializedObject(mp);
            smp.FindProperty("moveAxis").enumValueIndex = 1;   // Y
            smp.FindProperty("moveDistance").floatValue = 1.5f;
            smp.FindProperty("speed").floatValue = 0.8f;
            smp.ApplyModifiedProperties();

            Debug.Log("[FixPassage] OBS_FallingBlock: replaced MovableObs(X) with MovingPlatform(Y) at (52,10,0) ±1.5.");
            changed = true;
        }

        // ── S5_RoofSurface: trim left edge so it doesn't seal the S4 shaft ──
        // Old: center (66, 21, 0) scale (26, 0.5, 14) → x=[53,79]
        //      Bottom at y=20.75 = S4_Plat6 top (y=20.75).  Player on S4_Plat6
        //      has their body inside the slab and cannot jump.
        // New: center (71.5, 21, 0) scale (15, 0.5, 14) → x=[64,79]
        //      S4 shaft exit zone (x=58-64) is now open air.  Player jumps from
        //      S4_Plat6 (top y=20.75, x=60.8-63.2) up to S5_Jump1 (top y=21.95,
        //      x=58.8-61.2) with no ceiling obstruction.
        var roofSurface = GameObject.Find("S5_RoofSurface");
        if (roofSurface != null)
        {
            roofSurface.transform.position   = new Vector3(71.5f, 21f, 0f);
            roofSurface.transform.localScale = new Vector3(15f, 0.5f, 14f);
            EditorUtility.SetDirty(roofSurface);
            Debug.Log("[FixPassage] S5_RoofSurface trimmed to x=[64,79] — S4 exit zone now open.");
            changed = true;
        }

        if (changed)
        {
            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene);
            Debug.Log("[FixPassage] Done — all passage fixes applied. Press Play to test.");
        }
        else
        {
            Debug.Log("[FixPassage] No changes needed — scene already up to date.");
        }
    }
}
