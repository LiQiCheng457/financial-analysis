<template>
  <div class="management-team">
    <el-card shadow="hover">
      <div class="card-header">
        <h4>管理层</h4>
        <small class="sub">关键高管与联系方式</small>
      </div>

      <div class="team-grid">
            <div class="person" v-if="profile.legal_representative">
              <div class="role">法定代表人</div>
              <div class="name">{{ profile.legal_representative }}</div>
            </div>

        <div class="person" v-if="profile.chairman">
          <div class="role">董事长</div>
          <div class="name">{{ profile.chairman }}</div>
        </div>

        <div class="person" v-if="profile.general_manager">
          <div class="role">总经理</div>
          <div class="name">{{ profile.general_manager }}</div>
        </div>

        <div class="person" v-if="profile.board_secretary">
          <div class="role">董秘</div>
          <div class="name">{{ profile.board_secretary }}</div>
        </div>

        <div class="person contact" v-if="phone">
          <div class="role">联系电话</div>
          <div class="name">{{ phone }}</div>
        </div>

        <div class="person contact" v-if="email">
          <div class="role">电子邮箱</div>
          <div class="name">{{ email }}</div>
        </div>

        <!-- fallback: if none of the above present, show short profile summary -->
        <div class="no-data" v-if="!hasAny">
          <el-empty description="暂无管理层信息" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ profile: any }>()
const profile = props.profile || {}

const phone = computed(() => {
  return profile.contact_phone || profile.phone || profile.telephone || profile.mobile || ''
})

const email = computed(() => {
  return profile.email || profile.contact_email || profile.email_address || ''
})

const hasAny = computed(() => {
  return Boolean(profile && (
    profile.legal_representative || profile.chairman || profile.general_manager || profile.board_secretary || phone.value || email.value
  ))
})
</script>

<style scoped>
.management-team .card-header { display:flex; align-items:flex-end; gap:10px }
.management-team h4 { margin:0; font-size:16px }
.management-team .sub { color:var(--text-secondary); font-size:12px }
.team-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; margin-top:12px }
.person { background: #fff; border-radius:6px; padding:12px; border:1px solid #f0f0f0 }
.person .role { font-size:12px; color:#909399; margin-bottom:6px }
.person .name { font-size:15px; color:#303133; font-weight:600 }
.person.contact .name { font-weight:500; color:#409EFF }
.no-data { grid-column: 1 / -1; display:flex; justify-content:center; padding:12px }

@media (max-width: 720px) {
  .team-grid { grid-template-columns: 1fr }
}
</style>
